import threading
import json
import datetime
import shortuuid
import redis
import zlib
import base64
import traceback
import uuid
import re
import http.client

from collections import OrderedDict
from logging import getLogger, DEBUG
from concurrent_log_handler import ConcurrentRotatingFileHandler

import hmbtg_utils.hashing as humanhash
import hmbtg_utils.environment as env

logger = getLogger('hmbtg_events')
logger.setLevel(DEBUG)
logger.propagate = False

MAX_NUMBER_OF_EVENTS_IN_MEMORY=1000000

def reset_defaults():
    global MAX_NUMBER_OF_EVENTS_IN_MEMORY
    MAX_NUMBER_OF_EVENTS_IN_MEMORY=1000000


tl = threading.local()


if not len(logger.handlers):
    logfile = '/data/logs/ckanuser/ckanLogs/events.log'
    rotateHandler = ConcurrentRotatingFileHandler(logfile, "a", 5*1024*1024, 50)
    logger.addHandler(rotateHandler)


def utctimestamp():
    dt = datetime.datetime.utcnow()
    utc = (dt - datetime.datetime(1970, 1, 1)).total_seconds()
    return str(int(utc*10))

def error(msg=None, src=None, trace=None):
    n = env.process_name()
    etype = (n+'/'+src+'/err') if src else (n+'/err')
    keys = [['utc',utctimestamp()], ['type',etype]]
    
    if msg:
        keys.append(['msg',msg])
    if trace:
        comp =  base64.b64encode(zlib.compress(trace.encode('utf8')))
        keys.append(['ztrace',comp])

    # with open('/data/logs/ckanuser/ckanLogs/events.log', 'a+') as f:
    #     f.write(json.dumps(OrderedDict(keys))+'\n')
    logger.debug(json.dumps(OrderedDict(keys))+'\n')

def heartbeat(interval=0.1):
    _log('heartbeat', zdata=env.get_system_stats(interval))

def log(event, msg=None, zdata=None, data=None):
    _log(event, msg=msg, zdata=zdata, data=data)

def error(msg=None, src=None, trace=None):
    if not trace:
        tb = traceback.format_exc()
        if tb and tb != 'None\n':
            trace = tb
    if trace and not msg:
        msg = trace.split('\n')[-2]

    _log('err', msg=msg, src=src, trace=trace)

def _log(event, msg=None, src=None, trace=None, data=None, zdata=None):
    n = env.process_name()
    etype = n + '/' + event
    keys = [['utc',utctimestamp()], ['type',etype]]

    if hasattr(tl,'id'):
        keys.append(['id',tl.id])
    if msg:
        keys.append(['msg',noip(msg)])
    if trace:
        comp =  base64.b64encode(zlib.compress(noip(trace).encode('utf8'))).decode('utf8')
        keys.append(['ztrace',comp])
    if data:
        keys.append(['data', noip(json.dumps(data))])
    if zdata:
        comp =  base64.b64encode(zlib.compress(noip(json.dumps(zdata)).encode('utf8'))).decode('utf8')
        keys.append(['zdata',comp])

    # with open('/data/logs/ckanuser/ckanLogs/events.log', 'a+') as f:
    #     f.write(json.dumps(OrderedDict(keys))+'\n')

    j = OrderedDict(keys)
    data = json.dumps(j)
    logger.debug(data)

    _send_to_redis(data)
    _send_to_log_server(j)

def newContext(id=None):
    if not id:
        id = shortuuid.uuid()
    tl.id = id

def hostid():
    return humanhash.humanize(str(uuid.getnode()))

def _togelf(j):
    gelf = {}
    gelf['host'] = hostid()
    gelf['timestamp'] = float(j['utc'])/10
    gelf['short_message'] = j['type']

    if 'zdata' in j and j['type'] == 'schedule/heartbeat':
        data = json.loads(zlib.decompress(base64.b64decode(j['zdata'])).decode('utf8'))
        for k,v in list(data.items()):
            for k1, v1 in list(v.items()):
                gelf[k+'_'+k1] = float(v1)
    if 'zdata' in j and not (j['type'] == 'schedule/heartbeat'):
        data = json.loads(zlib.decompress(base64.b64decode(j['zdata'])).decode('utf8'))
        gelf['data'] = data

    if 'data' in j:
        gelf['data'] = j['data']

    if 'ztrace' in j:
        data = zlib.decompress(base64.b64decode(j['ztrace'])).decode('utf8')
        gelf['trace'] = data

    if 'msg' in j:
        gelf['long_message'] = j['msg']

    return json.dumps(gelf)

def _send_to_log_server(j):
    data = _togelf(j)
    try:
        connection = http.client.HTTPConnection(host='sarchiv-0007.vcac', port=80, timeout=5)
        connection.request("POST", '/gelf', data, {})
    except:
        with open('/data/logs/ckanuser/ckanLogs/errors.log', 'a+') as f:
            f.write('could not send log to log-server: ' + data)

def noip(msg):
    msg = re.sub(
        r"([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})", r"\1.\2.0.0", msg)
    msg = re.sub(
        r"([0-9]{1,3})-([0-9]{1,3})-([0-9]{1,3})-([0-9]{1,3})", r"\1-\2-0-0", msg)
    return msg

def _send_to_redis(data):
    try:
        r = _connect()
        r.lpush('events', data)
        r.ltrim('events', 0, MAX_NUMBER_OF_EVENTS_IN_MEMORY-1)
    except redis.RedisError as e:
        with open('/data/logs/ckanuser/ckanLogs/errors.log', 'a+') as f:
            f.write('could not send event to redis: ' + str(e))
            f.write(traceback.format_exc())
            f.write('event was:\n')
            f.write(data)

def _decode_event(evt):
    dt =  datetime.datetime.utcfromtimestamp(int(float(evt['utc'])/10))
    evt['utc'] =  dt.strftime('%Y-%m-%d %H:%M:%S')
    if 'ztrace' in evt:
        evt['trace'] = zlib.decompress(base64.b64decode(evt['ztrace'])).decode('utf8')
        del evt['ztrace']
    if 'zdata' in evt:
        evt['data'] = json.loads(zlib.decompress(base64.b64decode(evt['zdata'])).decode('utf8'))
        del evt['zdata']
    return evt

def last_events(count=-1, include=None, exclude=None):
    r = _connect()
    ret = []
    if exclude:
        exclude = re.compile('^' + exclude.replace('*','\w*')+'$')
    if include:
        include = re.compile('^' + include.replace('*','\w*')+'$')

    for evt in r.lrange( "events", 0, -1):
        if count == 0:
            return ret
        evt = json.loads(evt)
        if exclude and exclude.match(evt['type']):
            continue
        if include and not include.match(evt['type']):
            continue
        ret.append(_decode_event(evt))
        count-=1
    return ret

def empty_event_list():
    r = _connect()
    r.delete('events')

def _connect():
    return redis.StrictRedis(host="localhost", port=6379, db=0)
