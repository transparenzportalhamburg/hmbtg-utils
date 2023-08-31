import shlex
import subprocess
import sys

import hmbtg_utils.globals as g
from hmbtg_utils.environment import activate



def sh(command: str, wait=True, output=sys.stdout) -> None:
    """
        Runs a Command in the Shell.
    Args:
        command (str): The command that should be executed in shell.
        wait (bool, optional): if set True the command is blocking until its finished. Defaults to True.
        output (file_descriptor, optional): Provides an output for the running command. Defaults to sys.stdout.

    Raises:
        Exception: if wait is True it raises a Exeption in case of a command failture.
    """

    commands = shlex.split(command)

    if wait:
        process = subprocess.call(commands, stdout=output, stderr=output)
    # TODO: Error handeling
    else:
        subprocess.Popen(commands, stdout=output, stderr=output)

def run():
    pass

def run_ckan(command, wait=True, output=sys.stdout, config_name=g.CKAN_DEV_INI, activated=True):
    ckan = g.CKAN_EXE_PATH
    ckan_command = f"{ckan} --config={config_name} {command}"
    
    if activated:
        activate()

    result = run(command=ckan_command, wait=wait, output=output)
    
    return result


def run_ckan_command(command, wait=True, output=sys.stdout, config_name=g.CKAN_DEV_INI) -> None:
    """
    This Function runs a ckan command.
    Example: 
        run_ckan_command(command="search-index rebuild", config="/path/to/ckan_config")
        # ckan --config=/path/to/ckan_config search-index rebuild
    Args:
        command (_type_): 
        wait (bool, optional): if set True the command is blocking until its finished . Defaults to True.
        output (_type_, optional): Provides an output for the running command. Defaults to sys.stdout.
        config_name (str, optional): Path to the ckan config file. Defaults to "<CKAN_CONFIG_PATH>/development.ini" See globals.py.
    """

    ckan = g.CKAN_EXE_PATH
    ckan_command = f"{ckan} --config={config_name} {command}"

    sh(command=ckan_command, wait=wait, output=output)


def run_ckan_command_with_activate(command, wait=True, output=sys.stdout, config_name=g.CKAN_DEV_INI):
    """
        This Function runs a ckan command with active_this. <see hmbtg.environment.activate>
    Example: 
        run_ckan_command(command="search-index rebuild", config="/path/to/ckan_config")
        # ckan --config=/path/to/ckan_config search-index rebuild
    Args:
        command (_type_): 
        wait (bool, optional): if set True the command is blocking until its finished . Defaults to True.
        output (_type_, optional): Provides an output for the running command. Defaults to sys.stdout.
        config_name (str, optional): Path to the ckan config file. Defaults to "<CKAN_CONFIG_PATH>/development.ini" See globals.py.
    """
    activate()
    run_ckan_command(command, wait, output, config_name)
    