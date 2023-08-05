"""Provide utilities to help using the MySQL DB within the lz_drip package"""

import os

from drip import utils as drip_utils

_CONFIG_STRINGS = [
    "pipe_db_user",
    "pipe_db_password",
    "pipe_db_database",
    "pipe_db_host",
]
_USER_INDEX = 0
_PASSWORD_INDEX = _USER_INDEX + 1
_DATABASE_INDEX = _PASSWORD_INDEX + 1
_HOST_INDEX = _DATABASE_INDEX + 1
_CONFIG_INTEGERS = ["pipe_db_port"]
_PORT_INDEX = 0

_USER_ENVAR = "PIPE_DB_USER"
_PASSWORD_ENVAR = "PIPE_DB_PASSWORD"
_DATABASE_ENVAR = "PIPE_DB_DATABASE"
_HOST_ENVAR = "PIPE_DB_HOST"
_PORT_ENVAR = "PIPE_DB_PORT"

_DEFAULT_USER = "lzsalt"
_DEFAULT_DATABASE = "salt_pipeline"
_DEFAULT_HOST = "db-mysql"
_DEFAULT_PORT = 3306


def select_db_database(config: drip_utils.Configs) -> str:
    """
    Returns the database name of the DB.
    """
    if _DATABASE_ENVAR in os.environ:
        return os.environ[_DATABASE_ENVAR]
    config_key = _CONFIG_STRINGS[_DATABASE_INDEX]
    if config_key not in config or None is config[config_key]:
        return _DEFAULT_DATABASE
    return str(config[config_key])


def select_db_host(config: drip_utils.Configs) -> str:
    """
    Returns the host on which the DB is running.
    """
    if _HOST_ENVAR in os.environ:
        return os.environ[_HOST_ENVAR]
    config_key = _CONFIG_STRINGS[_HOST_INDEX]
    if config_key not in config or None is config[config_key]:
        return _DEFAULT_HOST
    return str(config[config_key])


def select_db_password(config: drip_utils.Configs) -> str:
    """
    Returns the password with which to access the DB.
    """
    if _PASSWORD_ENVAR in os.environ:
        return os.environ[_PASSWORD_ENVAR]
    config_key = _CONFIG_STRINGS[_PASSWORD_INDEX]
    if config_key not in config or None is config[config_key]:
        raise ValueError(
            "password must be defined in configuration file,"
            + " or envar "
            + _PASSWORD_ENVAR
            + " set"
        )
    return str(config[config_key])


def select_db_port(config: drip_utils.Configs) -> int:
    """
    Returns the User name with which to access the DB.
    """
    if _PORT_ENVAR in os.environ:
        return int(os.environ[_PORT_ENVAR])
    config_key = _CONFIG_INTEGERS[_PORT_INDEX]
    if config_key not in config or None is config[config_key]:
        return _DEFAULT_PORT
    return int(str(config[config_key]))


def select_db_user(config: drip_utils.Configs) -> str:
    """
    Returns the User name with which to access the DB.
    """
    if _USER_ENVAR in os.environ:
        return os.environ[_USER_ENVAR]
    config_key = _CONFIG_STRINGS[_USER_INDEX]
    if config_key not in config or None is config[config_key]:
        return _DEFAULT_USER
    return str(config[config_key])
