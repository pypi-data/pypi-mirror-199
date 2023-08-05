"""Provide utilities to help using files within the lz_drip package"""

import os
from pathlib import Path

from drip import utils as drip_utils

_CONFIG_STRINGS = ["source", "destination", "nosalt"]
_SOURCE_INDEX = 0
_DESTINATION_INDEX = _SOURCE_INDEX + 1
_NOSALT_INDEX = _DESTINATION_INDEX + 1
_CONFIG_INTEGERS = ["threshold"]
_THRESHOLD_INDEX = 0
_CONFIG_BOOLS = ["bypass", "park", "pipeline"]
_BYPASS_INDEX = 0
_PARK_INDEX = _BYPASS_INDEX + 1
_PIPELINE_INDEX = _PARK_INDEX + 1

_SOURCE_ENVAR = "FILE_DRIP_SOURCE"
_DESTINATION_ENVAR = "FILE_DRIP_DESTINATION"
_NOSALT_ENVAR = "FILE_DRIP_NOSALT"
_THRESHOLD_ENVAR = "FILE_DRIP_THRESHOLD"
_BYPASS_ENVAR = "FILE_DRIP_BYPASS"
_PARK_ENVAR = "FILE_DRIP_PARK"
_PIPELINE_ENVAR = "FILE_DRIP_PIPELINE"

_DEFAULT_THRESHOLD = 8
_DEFAULT_BYPASS = False
_DEFAULT_PARK = False
_DEFAULT_PIPELINE = False


def nersc_move(src: Path, dst: Path) -> None:
    """
    Move a file from src to dst. As NERSC does not allow ownership
    change, this function makes sure the owner of the dst is the user
    who executed it.

    Args:
        src: The file to be moved.
        dst: The destination file or directory.

    Raises:
        IOError: If the move has not been successfully completed.
    """
    return_code = os.system(f"cp -rp {src} {dst}")
    if 0 != return_code:
        raise IOError(f"Could not copy {src} to {dst}")
    os.remove(src)


def read_config(config_file: str, section: str) -> drip_utils.Configs:
    """
    Reads the supplied configuration ini file.

    Args:
        config_file: the path to the file containing the
                configuration information.
        section: the section within the file containing the
                configuration for this instance.

    Returns:
        A dict of key-value pairs for the specified section of the
                supplied file.
    """
    return drip_utils.read_config(
        config_file,
        section,
        booleans=_CONFIG_BOOLS,
        integers=_CONFIG_INTEGERS,
        strings=_CONFIG_STRINGS,
    )


def select_bypass(config: drip_utils.Configs) -> bool:
    """
    Returns True is the bundles should bypass salting.

    Args:
        config: The dict of key-value pairs from which to extract the
                threshold.

    Returns:
        True is the bundles should bypass salting.
    """
    if _BYPASS_ENVAR in os.environ:
        file_bypass = os.getenv(_BYPASS_ENVAR)
        if not file_bypass:
            raise ValueError(f"{_BYPASS_ENVAR} exist but has no value")
        return bool(file_bypass)
    config_key = _CONFIG_BOOLS[_BYPASS_INDEX]
    if config_key not in config or None is config[config_key]:
        return _DEFAULT_BYPASS
    return bool(config[config_key])


def select_destination(config: drip_utils.Configs) -> Path:
    """
    Returns the Path to the selected bundles destination.

    Args:
        config: The dict of key-value pairs from which to extract the
                destination.

    Returns:
        The path to the selected bundles destination.
    """
    if _DESTINATION_ENVAR in os.environ:
        return Path(os.environ[_DESTINATION_ENVAR])
    config_key = _CONFIG_STRINGS[_DESTINATION_INDEX]
    if config_key not in config or None is config[config_key]:
        raise ValueError(
            "destination must be defined in configuration file,"
            + " or envar "
            + _DESTINATION_ENVAR
            + " set"
        )
    destination = Path(str(config[config_key]))
    if not destination.exists():
        raise ValueError(f"{destination.resolve()} does not exist!")
    if not destination.is_dir():
        raise ValueError(f"{destination.resolve()} is not a directory")
    return destination


def select_nosalt(config: drip_utils.Configs) -> Path:
    """
    Returns the Path to the salt destination for non-salt bundles.

    Args:
        config: The dict of key-value pairs from which to extract the
                non-salt destination.

    Returns:
        The path to the salt destination for non-salt bundles
    """
    if _NOSALT_ENVAR in os.environ:
        return Path(os.environ[_NOSALT_ENVAR])
    config_key = _CONFIG_STRINGS[_NOSALT_INDEX]
    if config_key not in config or None is config[config_key]:
        raise ValueError(
            "nosalt must be defined in configuration file,"
            + " or envar "
            + _NOSALT_ENVAR
            + " set"
        )
    nosalt = Path(str(config[config_key]))
    if not nosalt.exists():
        raise ValueError(f"{nosalt.resolve()} does not exist!")
    if not nosalt.is_dir():
        raise ValueError(f"{nosalt.resolve()} is not a directory")
    return nosalt


def select_park(config: drip_utils.Configs) -> bool:
    """
    Returns True if the bundles should be parked while bypassing
    salting.

    Args:
        config: The dict of key-value pairs from which to extract the
                threshold.

    Returns:
        True if the bundles should be parked while bypassing salting.
    """
    if _PARK_ENVAR in os.environ:
        park_files = os.getenv(_PARK_ENVAR)
        if not park_files:
            raise ValueError(f"{_PARK_ENVAR} exists but has no value")
        return bool(park_files)
    config_key = _CONFIG_BOOLS[_PARK_INDEX]
    if config_key not in config or None is config[config_key]:
        return _DEFAULT_PARK
    return bool(config[config_key])


def select_pipeline(config: drip_utils.Configs) -> bool:
    """
    Returns True if the bundles should be pipelined while bypassing
    salting.

    Args:
        config: The dict of key-value pairs from which to extract the
                threshold.

    Returns:
        True if the bundles should be pipelined while bypassing
                salting.
    """
    if _PIPELINE_ENVAR in os.environ:
        pipeline_files = os.getenv(_PIPELINE_ENVAR)
        if not pipeline_files:
            raise ValueError(f"{_PIPELINE_ENVAR} exists but has no value")
        return bool(pipeline_files)
    config_key = _CONFIG_BOOLS[_PIPELINE_INDEX]
    if config_key not in config or None is config[config_key]:
        return _DEFAULT_PIPELINE
    return bool(config[config_key])


def select_source(config: drip_utils.Configs) -> Path:
    """
    Returns the Path to the selected bundles source.

    Args:
        config: The dict of key-value pairs from which to extract the
                source.

    Returns:
        The path to the selected bundles source.
    """
    if _SOURCE_ENVAR in os.environ:
        return Path(os.environ[_SOURCE_ENVAR])
    config_key = _CONFIG_STRINGS[_SOURCE_INDEX]
    if config_key not in config or None is config[config_key]:
        raise ValueError(
            "source must be defined in configuration file,"
            + " or envar "
            + _SOURCE_ENVAR
            + " set"
        )
    source = Path(str(config[config_key]))
    if not source.exists():
        raise ValueError(f"{source.resolve()} does not exist!")
    return source


def select_threshold(config: drip_utils.Configs) -> int:
    """
    Returns the threshold under which transfers can continue.

    Args:
        config: The dict of key-value pairs from which to extract the
                threshold.

    Returns:
        The threshold under which transfers can continue.
    """
    if _THRESHOLD_ENVAR in os.environ:
        file_threshold = os.getenv(_THRESHOLD_ENVAR)
        if not file_threshold:
            raise ValueError(f"{_THRESHOLD_ENVAR} exist but has no value")
        return int(file_threshold)
    config_key = _CONFIG_INTEGERS[_THRESHOLD_INDEX]
    if config_key not in config or None is config[config_key]:
        return _DEFAULT_THRESHOLD
    return int(str(config[config_key]))
