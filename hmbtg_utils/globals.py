
#COMMON
DATA_DIR = "/data"
TMP_DIR = f"{DATA_DIR}/tmp"
OPT_DIR = f"{DATA_DIR}/opt"
VAR_DIR = f"{DATA_DIR}/var"
LOG_DIR = f"{DATA_DIR}/logs"
CONFIG_DIR = f"{DATA_DIR}/config"
DEPLOYMENT_DIR = f"{DATA_DIR}/deployment"

#SOLR 
SOLR_OPT = f"{OPT_DIR}/solr"
SOLR_VAR = f"{VAR_DIR}/solr"
SOLR_DATA_DIR = f"{SOLR_VAR}/data"
SOLR_CKAN_CORE = f"{SOLR_DATA_DIR}/ckan"
SOLR_XML = f"{SOLR_DATA_DIR}/solr.xml"
SOLR_VERSION = "8.11.2"


#HMBTG


#CKAN
CKAN_BASE_PATH = f"{DATA_DIR}/ckan"
CKAN_VAR_PATH = f"{CKAN_BASE_PATH}/var"
CKAN_LIB_PATH = f"{CKAN_BASE_PATH}/lib"
CKAN_ETC_PATH = f"{CKAN_BASE_PATH}/etc"

HMBTG_VENV_PATH = f"{CKAN_LIB_PATH}/default"

CKAN_CONFIG_PATH = f"{CKAN_ETC_PATH}/default"
CKAN_EXE_PATH = f"{HMBTG_VENV_PATH}/bin/ckan"


ACTIVATE_THIS_FILE = f"{HMBTG_VENV_PATH}/bin/activate_this.py"


#INIs
ENV_INI = f"{DATA_DIR}/env.ini"
HMBTG_INI = f"{CKAN_CONFIG_PATH}/hmbtg.ini"
CKAN_WEB_INI = f"{CKAN_CONFIG_PATH}/web.ini"
CKAN_DEV_INI = f"{CKAN_CONFIG_PATH}/development.ini"


#PROJECTS
PROJECT_SOURCE_FOLDER = f"{HMBTG_VENV_PATH}/src"
HMBTG_UTILS_ROOT = f"{PROJECT_SOURCE_FOLDER}/hmbtg-utils"
HMBTG_CONFIG_ROOT = f"{PROJECT_SOURCE_FOLDER}/hmbtg-config"
HMBTG_SCRIPTS_ROOT = f"{PROJECT_SOURCE_FOLDER}/scripts"

CKAN_EXTENTION_FULLTEXT_ROOT = f"{PROJECT_SOURCE_FOLDER}/ckanext-fulltext"
CKAN_EXTENTION_DISTRIBUTED_HARVEST_ROOT = f"{PROJECT_SOURCE_FOLDER}/ckanext-distributed-harvest/"
CKAN_EXTENTION_HMBTGHARVESTERS_ROOT = f"{PROJECT_SOURCE_FOLDER}/ckanext-hmbtgharvesters"
CKAN_EXTENTION_HIGHLIGTHING_ROOT = f"{PROJECT_SOURCE_FOLDER}/ckanext-highlighting"
CKAN_EXTENTION_FULLTEXT_ROOT = f"{PROJECT_SOURCE_FOLDER}/ckanext-fulltext"

#TEMPLATES
TEMPLATE_DIR = f"{HMBTG_UTILS_ROOT}/hmbtg-utils/templates"
ENV_INI_TEMPLATE = f"{TEMPLATE_DIR}/env.ini"


#SOLR

