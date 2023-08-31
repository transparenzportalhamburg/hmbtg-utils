from configparser import ConfigParser
from typing import Dict, List
import hmbtg_utils.globals as g


CONFIG_TABLE = {
    "hmbtg-ini": g.HMBTG_INI,
    "web-ini": g.CKAN_WEB_INI,
    "devel-ini": g.CKAN_DEV_INI,
    "env-ini": g.ENV_INI
}


def show_config_types() -> List[str]:
    """ Returns a list of known config files.

    Returns:
        List[str]: list of known config keys.
    """
    return list(CONFIG_TABLE.keys)


def config_to_dict(config: ConfigParser) -> Dict[str, Dict[str, str]]:
    """ Converts a config to a dict.
    Note: It adds the DEFAULT to the Sections.

    Args:
        config (ConfigParser): to parse config.

    Returns:
        Dict[str, Dict[str, str]]: converted config.
    """
    result = {}
    sections = config.sections()
    sections.append("DEFAULT")

    for section in sections:
        section_data = {}
        for key, value in config.items(section):
            section_data.update({key: value})
        result.update({section: section_data})

    return result

def load_config(file_path: str)-> dict:
    """Loads a config from file.

    Args:
        file_path (str): the path and file
    Returns:
        dict: _description_
    """
    config = ConfigParser(interpolation=None)
    config.read(file_path)
    config = config_to_dict(config)
    return config

def get_config(name: str) -> Dict[str, Dict[str, str]]:
    """ Loads config by key name.
    Args:
        name (str): config key

    Returns:
        Dict[str, Dict[str, str]]: the config.
    """
    file_path = CONFIG_TABLE.get(name, "")
    config = load_config(file_path=file_path)
    
    return config
