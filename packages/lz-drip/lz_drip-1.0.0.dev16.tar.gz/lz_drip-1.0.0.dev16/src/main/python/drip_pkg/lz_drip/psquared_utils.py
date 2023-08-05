"""Provide utilities to help using psquared within the lz_drip package"""

from typing import Optional

import os

from drip import utils as drip_utils

_CONFIG_STRINGS = ["url", "configuration", "version", "scheduler"]
_URL_INDEX = 0
_CONFIGURATION_INDEX = _URL_INDEX + 1
_CONFIG_VERSION_INDEX = _CONFIGURATION_INDEX + 1
_SCHEDULER_INDEX = _CONFIG_VERSION_INDEX + 1

_URL_ENVAR = "PP_APPLICATION"
_CONFIGURATION_ENVAR = "PP_CONFIGURATION"
_CONFIG_VERSION__ENVAR = "PP_CONFIG_VERSION"
_SCHEDULER_ENVAR = "PP_SCHEDULER"


def select_url(config: drip_utils.Configs) -> str:
    """
    Returns the URL of the PSquared web service.
    """
    if _URL_ENVAR in os.environ:
        return os.environ[_URL_ENVAR]
    config_key = _CONFIG_STRINGS[_URL_INDEX]
    if config_key not in config or None is config[config_key]:
        raise ValueError(
            "url for PSquared must be defined in configuration file,"
            + " or envar "
            + _URL_ENVAR
            + " set"
        )
    return str(config[config_key])


def select_configuration(config: drip_utils.Configs) -> str:
    """
    Returns the PSquared configuration to use when submitting to the Salting Sercvice
    """
    if _CONFIGURATION_ENVAR in os.environ:
        return os.environ[_CONFIGURATION_ENVAR]
    config_key = _CONFIG_STRINGS[_CONFIGURATION_INDEX]
    if config_key not in config or None is config[config_key]:
        raise ValueError(
            "PSquared configuration must be defined in configuration file,"
            + " or envar "
            + _CONFIGURATION_ENVAR
            + " set"
        )
    return str(config[config_key])


def select_config_version(config: drip_utils.Configs) -> str:
    """
    Returns the version of the PSquared configuration to use when submitting to the
    Salting Sercvice
    """
    if _CONFIG_VERSION__ENVAR in os.environ:
        return os.environ[_CONFIG_VERSION__ENVAR]
    config_key = _CONFIG_STRINGS[_CONFIG_VERSION_INDEX]
    if config_key not in config or None is config[config_key]:
        raise ValueError(
            "Version of psquared configuration must be defined in configuration file,"
            + " or envar "
            + _CONFIG_VERSION__ENVAR
            + " set"
        )
    return str(config[config_key])


def select_scheduler(config: drip_utils.Configs) -> Optional[str]:
    """
    Returns the Path to the selected file threshold
    """
    if _SCHEDULER_ENVAR in os.environ:
        return os.environ[_SCHEDULER_ENVAR]
    config_key = _CONFIG_STRINGS[_SCHEDULER_INDEX]
    if config_key not in config or None is config[config_key]:
        return None
    return str(config[config_key])
