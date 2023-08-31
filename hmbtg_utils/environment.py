import os
import re
import psutil
import subprocess

import hmbtg_utils.globals as g
import hmbtg_utils.config as c


def create_env(source_dir=g.ENV_INI_TEMPLATE, target_dir=g.ENV_INI, **kwargs) -> None:
    """Creates env.ini with parameters. 
    Throws KeyError if a parameter is missing. For needed params check hmbtg-utils/templates/env.ini
    """

    with open(source_dir, "r") as f:
        env = f.read()

    with open(target_dir, "w+") as f:
        env.format(**kwargs)
        f.write(env)


def load_env(target_dir=g.ENV_INI) -> dict:
    """Loads env.ini and stores all variables in a dict.

    Returns:
        dict: with all DEFAULT vars.
    """
    return c.load_config(target_dir).get("DEFAULT")


def load_hmbtg_ini() -> dict:
    """Loads the hmbtg.ini.

    Returns:
        dict: _description_
    """
    return c.get_config("hmbtg-ini")


def load_web_ini() -> dict:
    """Loads the web.ini.

    Returns:
        dict: _description_
    """
    return c.get_config("web-ini")


def ckan_site_url(ini_type: str = "web-ini") -> str:
    """Returns the ckan.site_url. 
    Args:
        ini_type (str, optional): _description_. Defaults to "web-ini".

    Returns:
        str: _description_
    """
    config = c.get_config(f"{ini_type}-ini", {})
    app_main = config.get('app:main', {})

    return app_main.get('ckan.site_url')


def load_dev_ini() -> dict:
    """Loads the development.ini.

    Returns:
        dict: _description_
    """
    return c.get_config("development-ini")


def is_root() -> bool:
    """
    Checks if program is running as root.

    Returns:
        bool: True if programm is running as root False if not.
    """
    return os.geteuid() == 0


def is_master() -> bool:
    """Checks if the this system is a master system.

    Returns:
        bool: _description_
    """
    return load_env().get("kind") == "master"


def is_slave() -> bool:
    """Checks if the this system is a slave system.

    Returns:
        bool: _description_
    """
    return load_env().get("kind") == "slave"


def is_db() -> bool:
    """Checks if the this system is a db system.

    Returns:
        bool: _description_
    """
    return load_env().get("kind") == "db"


def is_docker() -> bool:
    """Checks if the this system is a docker container.

    Returns:
        bool: _description_
    """
    return


def activate() -> None:
    """
    Activates Virtualenv.
    """
    activate_this = os.path.join(g.ACTIVATE_THIS_FILE)
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})


processes = [
    # ['bulk', 'paster --plugin=ckan jobs worker bulk'],
    # ['priority', 'paster --plugin=ckan jobs worker priority'],
    ['fulltext', 'fulltext work'],
    ['fulltext_collect', 'fulltext process'], 
    ['repair_versions', 'hmbtg repair_package_versions'],
    ##['schedule', '/data/deployment/schedule.py'],
    ##['schedule_harvester', '/data/deployment/schedule_harvester.py'],
    ['fetch', 'distributed-harvester start-distributed-fetch-consumer'],
    ['gather', 'distributed-harvester start-distributed-gather-consumer'],
    ##['redis', 'redis-server'],
    ##['rabbitmq', 'rabbitmq-server'],
    ##['apache', 'apache'],
    ##['solr', 'solr/server'],
    ##['tika', 'tika.server'],
    ##['supervisord', 'supervisord'],
    ##['web', 'ckan_default      -k start'],
    ['command', 'command_worker.py'],
    ['reindex', 'reindex_worker.py']
]


def get_system_stats(interval=0.1):
    def to_str(d):
        return "%.02f" % d

    lines = subprocess.check_output(
        ['ps', '-aux']).decode('utf8').split('\n')[1:]
    ret = {}
    for n, p in processes:
        hits = list(filter((lambda l: l.count(p)), lines))
        cpu = 0
        mem = 0
        for h in hits:
            pid = int(re.split('\s+', h)[1])
            try:
                cpu += psutil.Process(pid).cpu_percent(interval=interval)
                mem += psutil.Process(pid).memory_percent()
            except psutil.NoSuchProcess:
                pass
        ret[n] = {'count': len(hits), 'cpu': to_str(cpu), 'mem': to_str(mem)}
    ret['total'] = {'cpu': to_str(psutil.cpu_percent(
        interval=interval)), 'mem': to_str(psutil.virtual_memory().percent)}
    return ret


def full_process_name():
    return ' '.join(psutil.Process().cmdline())


def process_name():
    f = full_process_name()
    for n, p in processes:
        if p in f:
            return n
    return psutil.Process().name()
