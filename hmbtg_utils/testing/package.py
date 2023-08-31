import time
import uuid
import os
import json

import ckan.tests.helpers as helpers
import ckan.tests.factories as factories
import ckanext.harvest.tests.factories as hfactories

from ckan.logic import get_action
from ckan.model import Session
from ckan.logic import get_action
from ckan.lib.search.index import PackageSearchIndex
from ckanext.harvest.model import HarvestObject
from ckan import model

from nose.tools import assert_equal

#from ckanext.hmbtgharvesters.service import package_service
#from ckanext.hmbtgharvesters.daos import harvest_dao


def wait_until(condition, timeout=60*10, granularity=5, time_factory=time):
    end_time = time.time() + timeout
    status, line = condition()
    while not status and time.time() < end_time:
        time.sleep(granularity)
        status, line = condition()
    if not status:
        raise Exception('timeout on waiting for condition')
    return line


def get_context():
    context = {
        'model': model,
        'session': Session,
        'ignore_auth': False,
        'user': 'sysadmin',
        'use_cache': False
    }
    return context


def commit_index():
    PackageSearchIndex().commit()


def get_package_from_index(id, timeout=20):
    def get():
        commit_index()
        context = {'ignore_auth': True, 'use_cache': False}
        r = helpers.call_action('package_search', q='id:{0}'.format(
            id), context=context)['results']
        return (len(r) > 0, r)

    wait_until(get, timeout=timeout, granularity=0.5)
    r = get()
    if len(r):
        assert len(r[1]) == 1
        return r[1][0]
    return None


def get_package_with_title(title, wait=None):
    context = {'ignore_auth': True}
    return helpers.call_action('package_search', q='title:{0}'.format(title),
                               context=context)['results']


def create_harvest_object(moi, pkgid, date, source):
    job = hfactories.HarvestJobObj(source=source)
    job.save()
    hdb = HarvestObject(guid=moi,
                        job=job,
                        current=True,
                        package_id=pkgid,
                        state='COMPLETE',
                        import_started=date)
    hdb.save()
    Session.commit()
    return hdb


def create_harvest_object_with_content(moi, content):
    job = hfactories.HarvestJobFactory()
    job.save()
    hdb = HarvestObject(guid=moi, job=job, current=True, content=content)
    hdb.save()
    Session.commit()
    return hdb


def create_harvest_object_with_content_from_file(old_moi, filename):
    moi = str(uuid.uuid4())
    filename = os.path.join(os.path.dirname(__file__), 'data/' + filename)

    content = None
    with open(filename) as h:
        content = h.read()
        content = content.replace(old_moi, moi)

    return create_harvest_object_with_content(moi, content.decode('utf-8').encode('utf-8'))


def create_indexed_dataset(**args):
    # if 'id' not in args:
    #     guid = str(uuid.uuid4())
    #     args['id'] = guid
    #     args['name'] = guid
    args['extras'] = [{'key': 'latestVersion', 'value': 'true'}]
    pkg = factories.Dataset(**args)
    commit_index()
    return pkg


def create_dataset_repair_fulltext(**args):
    guid = str(uuid.uuid4())
    guid_res = str(uuid.uuid4())
    args['extras'] = [{'key': 'latestVersion', 'value': 'true'}]
    args['state'] = 'active'
    args['title'] = 'fulltext_test_dataset'
    args['id'] = guid
    args['name'] = guid
    pkg = factories.Dataset(**args)
    resource = factories.Resource(package_id=guid, id=guid_res, name=guid_res,
                                  url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf', fulltext='ERROR_FULLTEXT', format='pdf')
    commit_index()
    return pkg


def create_dataset_dict(moi='moi', latestVersion=True, state='active', title='default_test_dataset', **args):
    guid = str(uuid.uuid4())
    args['id'] = guid
    args['name'] = args['name'] if 'name' in args else guid
    args['title'] = title
    args['state'] = state
    if not 'author' in args:
        args['author'] = 'test_author'
    args['groups'] = [{
        # 'display_name': "Infrastruktur, Bauen & Wohnen",
        # 'description': "",
        # 'title': "Infrastruktur, Bauen & Wohnen",
        # 'image_display_url': "",
        # 'id': "469b4869-114e-45eb-b168-c9a0bb00e1c9",
        'name': "infrastruktur-bauen-und-wohnen"
    }]
    args['extras'] = [
        {
            'key': 'source',
            'value': 'test_source'
        },
    ]
    args['maintainer'] = "BA Hamburg-Nord, IT-Angelegenheiten der Bezirksverwaltung"
    args['maintainer_email'] = "test@foo.bar"
    args['license_id'] = "dl-de-by-2.0"
    args['type'] = "document"
    args['owner_org'] = "hmdklgv"

    return args


def create_dataset(moi='moi', latestVersion=True, state='active', title='default_test_dataset', mainDocument=True, resource=None, extras=[], **args):
    args = create_dataset_dict(moi, latestVersion, state, title, **args)
    args['extras'] = [
        {
            'key': 'metadata_original_id',
            'value': moi
        },
        {
            'key': 'latestVersion',
            'value': 'true' if latestVersion else 'false'
        },
        {
            'key': 'mainDocument',
            'value': 'true' if mainDocument else 'false'
        }, *extras
    ]
    pkg = factories.Dataset(**args)
# def create_dataset(moi, latestVersion=True, state='active', title='default_test_dataset', resource=None, name=None, notes=None):
#     guid = str(uuid.uuid4())
#     pkg = factories.Dataset(id=guid,
#                             name=name if name else guid,
#                             title=title,
#                             state=state,
#                             notes=notes,
#                             extras=[
#                                 {
#                                     'key': 'metadata_original_id',
#                                     'value': moi
#                                 },
#                                 {
#                                     'key': 'latestVersion',
#                                     'value': 'true' if latestVersion else 'false'
#                                 },
#                                 {
#                                     'key': 'mainDocument',
#                                     'value': 'true'
#                                 },
#                             ])
    guid_res = str(uuid.uuid4())
    factories.Resource(package_id=pkg['id'], id=guid_res, name=guid_res,
                       url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf', fulltext=title + ' fulltext', format='pdf')
    return pkg


def get_package(id, validate=False):
    get_package = get_action('package_show')
    context = get_context()
    context['validate'] = False
    pkg = get_package(context, {"id": id})
    return pkg


def create_relationship(subject_id, object_id):
    func = get_action('package_relationship_create')
    data_dict = {'subject': subject_id, 'object': object_id,
                 'type': 'child_of', 'comment': ''
                 }
    context = {
        'model': model,
        'session': Session,
        'ignore_auth': False,
        'user': 'sysadmin',
        'validate': False,
        'defer_commit': False
    }
    func(context, data_dict)


def create_ho_with_package(moi, datetime, latestVersion=True, pstate='active'):
    pkg = create_dataset(moi, latestVersion, pstate)
    h1 = create_harvest_object(moi, pkg['id'], datetime)
    return pkg


def load_package(id):
    hos = Session.query(HarvestObject).filter(HarvestObject.id == id).all()
    assert_equal(len(hos), 1)
    pid = hos[0].package_id
    return get_action('package_show')({'ignore_auth': True}, {'id': pid})


def index_package(pkg):
    package_index = PackageSearchIndex()
    package_index.index_package(pkg, defer_commit=True)
    commit_index()
    return get_package_from_index(pkg['id'])


def search_package(term: str, timeout: int = 5):
    context = {'ignore_auth': True}

    def get():
        r = helpers.call_action('package_search', q=term,
                                context=context)['results']
        return (len(r) > 0, r)
    wait_until(get, timeout=timeout, granularity=0.5)
    return get()[1]


def load_default_test_pkg(**kwargs):
    pkg = json.load(
        open(os.path.join(os.path.dirname(__file__), 'data/index_pkg_01.json')))
    return {**pkg, **kwargs}

# def create_pkg_via_service(pkg):
#    return package_service.create_or_update_package(harvest_dao.harvest_source_from_title('HMDK').id, pkg)
