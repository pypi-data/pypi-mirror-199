"""
Provide command line access to the information about a Bundle that is
passing through in the Salt Pipeline.
"""

from typing import Dict, Optional, Tuple

import argparse
import xml.etree.ElementTree as ET
import logging
import os
from pathlib import Path
import sys
from zlib import adler32

from drip import utils as drip_utils
from lz_drip import PipelineDB

from lz_drip.file_utils import (
    read_config,
)
from lz_drip.mysql_utils import (
    select_db_user,
    select_db_password,
    select_db_database,
    select_db_host,
    select_db_port,
)

_LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}

_ENVARS_MAPPING = {
    "PIPELINE_INI_FILE": "INI_FILE",
    "PIPELINE_INI_SECTION": "INI_SECTION",
    "PIPELINE_LOG_FILE": "LOG_FILE",
    "PIPELINE_LOG_LEVEL": "LOG_LEVEL",
}

_ADLER32_BLOCKSIZE = 256 * 1024 * 1024


def _create_argument_parser() -> argparse.ArgumentParser:
    """
    Creates and populated the argparse.ArgumentParser for this executable.
    """
    parser = argparse.ArgumentParser(
        description="Updates the pipeline DB on the occasion a bundle exits the pipeline"
    )
    parser.add_argument(
        "--log_file",
        dest="LOG_FILE",
        help="The file, as opposed to stdout, into which to write log messages",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        default="INFO",
        dest="LOG_LEVEL",
        help="The logging level for this execution",
        choices=_LOG_LEVELS.keys(),
    )
    parser.add_argument(
        "-i",
        "--drip_ini",
        dest="INI_FILE",
        help="The path to the configuration file for the drip.Dropper class,"
        + " the default is $HOME/"
        + drip_utils.DEFAULT_INI_FILE,
    )
    parser.add_argument(
        "-s",
        "--ini_section",
        dest="INI_SECTION",
        default="drip_feed",
        help="The section of the INI file to use for this execution,"
        + ' the default is "drip_feed"',
    )
    parser.add_argument(
        dest="parked_directory",
        help="The directory holding the data file at the beginning of the salting pipeline",
    )
    parser.add_argument(
        dest="salted_directory",
        help="The directory holding the data file at the end of the salting pipeline",
    )
    parser.add_argument(
        dest="bundle_name",
        nargs=argparse.REMAINDER,
        help="The name of the Bundle exiting the pipeline",
    )
    return parser


def _read_envar_values(mapping: Dict[str, str]):
    """
    Create a argparse.Namespace instance populated by the values of the
    envrionmental variables specified by the keys of the mapping.
    """
    result = {}
    for key in mapping.keys():
        value = os.getenv(key)
        if None is not value:
            option = mapping[key]
            result[option] = value
    return argparse.Namespace(**result)


def _adler32(filename: Path) -> int:
    running_sum = 1
    with open(filename, "rb") as open_file:
        while True:
            data = open_file.read(_ADLER32_BLOCKSIZE)
            if not data:
                return running_sum
            running_sum = adler32(data, running_sum)
            if running_sum < 0:
                running_sum += 2**32


def _rebuild_metadata(
    metadata_path: Path, exit_checksum: int
) -> Tuple[ET.ElementTree, Optional[int]]:
    """
    Rebuild the metadata content to reflect existing the pipeline.
    """
    metadata_tree = ET.parse(metadata_path)
    metadata_element = metadata_tree.getroot()
    salt_pipelined = ET.Element("salt_pipelined")
    metadata_element.append(salt_pipelined)

    adler32_checksum: Optional[int] = None
    checksum_checksum: Optional[int] = None

    adler32_element = metadata_element.find("adler32")
    if None is not adler32_element:
        value = adler32_element.text
        if None is not value:
            adler32_checksum = int(value)
        adler32_element.text = str(exit_checksum)
    checksum_element = metadata_element.find('checksum[@algorithm="Adler32"]')
    if None is not checksum_element:
        value = checksum_element.text
        if None is not value:
            checksum_checksum = int(value)
        checksum_element.text = str(exit_checksum)
    if (
        None is not adler32_checksum
        and None is not checksum_checksum
        and adler32_checksum != checksum_checksum
    ):
        raise ValueError(
            f'Mismatched checksums in original metadata at "{metadata_path}"'
        )
    if None is adler32_checksum:
        return metadata_tree, checksum_checksum
    return metadata_tree, adler32_checksum


def execute(
    pipeline_db: PipelineDB, name: str, parked_directory: Path, salted_directory: Path
) -> None:
    """
    Manages the exit of a bundle into the "salted" area.

    Args:
        pipeline_db: The PipelineDB to use and update.
        name: The name of the bundle exiting.
        salted_directory: The path to the "salted" directory.
    """
    (
        parked_data_path,
        parked_metadata_path,
        parked_done_path,
        data_name,
    ) = pipeline_db.parked_paths(name)

    print(parked_data_path, parked_metadata_path, parked_done_path, data_name)
    salted_data_path = salted_directory.joinpath(parked_data_path.name)
    exit_checksum = _adler32(salted_data_path)
    metadata_tree, entry_checksum = _rebuild_metadata(
        parked_directory.joinpath(parked_metadata_path), exit_checksum
    )

    bundle_data_path = salted_directory.joinpath(data_name)
    salted_data_path.rename(bundle_data_path)

    salted_metadata_path = salted_directory.joinpath(parked_metadata_path.name)
    metadata_tree.write(salted_metadata_path)

    salted_done_path = salted_directory.joinpath(parked_done_path.name)
    salted_done_path.touch()
    pipeline_db.bundle_exit(name, entry_checksum, exit_checksum)


def main() -> int:
    """
    Main routine that access the information about a Bundle that is
    passing through in the Salt Pipeline.
    """
    parser = _create_argument_parser()
    envar_values = _read_envar_values(_ENVARS_MAPPING)
    options = parser.parse_args(namespace=envar_values)

    if None is options.LOG_FILE:
        logging.basicConfig(stream=sys.stdout, level=_LOG_LEVELS[options.LOG_LEVEL])
    else:
        logging.basicConfig(
            filename=options.LOG_FILE, level=_LOG_LEVELS[options.LOG_LEVEL]
        )

    logging.debug("Begin options:")
    for option in options.__dict__:
        if options.__dict__[option] is not None:
            logging.debug("    %s = %s", option, options.__dict__[option])
    logging.debug("End options:")

    config = read_config(drip_utils.find_config(options.INI_FILE), options.INI_SECTION)
    pipeline_db = PipelineDB(
        select_db_user(config),
        select_db_password(config),
        select_db_database(config),
        select_db_host(config),
        select_db_port(config),
    )
    pipeline_db.begin_transaction()
    for bundle in options.bundle_name:
        execute(
            pipeline_db,
            bundle,
            Path(options.parked_directory),
            Path(options.salted_directory),
        )
    pipeline_db.end_transaction()
    pipeline_db.close()
    return 0


if __name__ == "__main__":
    main()
