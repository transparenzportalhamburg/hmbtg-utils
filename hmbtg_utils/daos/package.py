import logging
from ckan.model import Session, Package, Group

logger = logging.getLogger(__name__)

def package_active_count():
    return Session.execute("select count(*) from package where state = 'active'").first()[0]


def get_package(id, session=None):
    if not session:
        session = Session
    package = session.query(Package).filter(Package.id == id).all()
    logger.debug('get_package for id: %s' % id)
    logger.debug('package: %s' %package)
    if len(package) > 1:
        logger.debug('Warning: Anzahl packages found: %s' % len(package))
    return package[0]

def package_count(session=None):
    if not session:
        session = Session
    return session.query(Package).count()


# def get_package_from_moi(moi, session=None):
#     if not session:
#         session = Session
#     package = session.query(Package).filter(Package.id == id).all()
#     if len(package) > 1:
#         logger.debug('Warning: Anzahl packages found: %s' % len(package))
#     return package[0]

#  Session.execute("select package_id from package_extra, package  where package_extra.package_id = package.id and package.state = 'active' and package.type = 'dataset' and package_extra.key = 'metadata_origi
# nal_id' and package_extra.value = '071c267d-7f35-4a4b-9c99-a57407a52416'").fetchall()


def package_name_free(name):
    return Session.execute("select count(name) from Package where name = '%s'" %name).first()[0] == 0

def get_max_package_name_suffix(name) :
    return Session.execute("select max(q.d) from (SELECT cast(nullif((regexp_matches(name,'^%s(\d*)'))[1],'') as integer) as d FROM package) as q" % name).fetchall()[0][0]

def is_package_in_group(group_name, package_id):
    group = Session.query(Group).filter(Group.name == group_name).first()
    for p in group.packages():
        if p.id == package_id:
            return True
    return False
