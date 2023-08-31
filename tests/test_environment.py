import os
import pytest
from tempfile import NamedTemporaryFile
import hmbtg_utils.environment as e


ENV_TEMPLATE = "./hmbtg_utils/templates/env.ini"
TEST_PARAMS = {"db_host": "test_db",
               "db_name_ckan": "test_db_name",
               "db_pass": "db_pass",
               "db_user": "db_user",
               "master_ip_external": "master_ip_external",
               "master_ip_internal": "master_ip_internal",
               "public_hmbtg_domain": "public_hmbtg_domain",
               "slave_ip_external": "slave_ip_external",
               "slave_ip_internal": "slave_ip_internal",
               "kind": "kind",
               "proxy_ip": "proxy_ip",
               "proxy_port": "proxy_port",
               "env": "env"}


def test_create_env():
    with NamedTemporaryFile() as f:
        e.create_env(source_dir=ENV_TEMPLATE,
                     target_dir=f.name,
                     **TEST_PARAMS)

        assert "proxy_port" in str(f.read())


def test_load_env():
    with NamedTemporaryFile() as f:
        target_dir = f.name
        e.create_env(source_dir=ENV_TEMPLATE,
                     target_dir=target_dir,
                     **TEST_PARAMS)
        env = e.load_env(target_dir)

    assert "proxy_port" in env


def test_create_env_with_missing():
    removed_key = "proxy_port"
    params = TEST_PARAMS.copy()
    del params[removed_key]

    result = ""
    with NamedTemporaryFile() as f:
        try:
            e.create_env(source_dir=ENV_TEMPLATE,
                         target_dir=f.name,
                         **params)
        except KeyError as exception:
            result = str(exception)

    assert result == f"'{removed_key}'"
