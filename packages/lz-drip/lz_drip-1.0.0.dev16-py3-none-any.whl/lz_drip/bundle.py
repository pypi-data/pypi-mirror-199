"""Define the Bundle class"""

from typing import List, Optional

import logging
import os
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

from .file_utils import nersc_move

_V4_VERSION = "v4"
_DATA_CATEGORY = "DATA"
_DONE_CATEGORY = "DONE"
_META_DATA_CATEGORY = "METADATA"

_DONE_FILE_PATTERN = "v4*DONE*"
_SPADE_FILE_PATTERN = (
    "^("
    + _V4_VERSION
    + ")_([0-9]*)_("
    + _DATA_CATEGORY
    + "|"
    + _DONE_CATEGORY
    + "|"
    + _META_DATA_CATEGORY
    + ")_([^_]*)_(.*)$"
)
_VERSION_INDEX = 1
_TICKET_INDEX = _VERSION_INDEX + 1
_FILECATEGORY_INDEX = _TICKET_INDEX + 1
_REGISTRATION_INDEX = _FILECATEGORY_INDEX + 1
_BUNDLE_INDEX = _REGISTRATION_INDEX + 1


class Bundle:
    """
    This class gathers together the three files that make up a SPADE bundle.
    """

    def __init__(self, done_file: Path):
        """
        Creates an instance of this class.

        Args:
            done_file: The Path to the DONE file of the bundle.
        """

        if not done_file.exists():
            raise ValueError("The supplied ' + _DONE_CATEGORY + ' file does not exist")
        parts = re.match(_SPADE_FILE_PATTERN, done_file.name)
        if parts is None:
            raise ValueError("The supplied file is not a DONE file")
        if parts.group(_FILECATEGORY_INDEX) != _DONE_CATEGORY:
            raise ValueError("The supplied file is not a DONE file")
        self.__bundle = parts.group(_BUNDLE_INDEX)
        parent = done_file.parent
        self.__done_file = done_file
        self.__meta_file = parent.joinpath(
            parts.group(_VERSION_INDEX)
            + "_"
            + parts.group(_TICKET_INDEX)
            + "_"
            + _META_DATA_CATEGORY
            + "_"
            + self.__bundle
            + ".meta.xml"
        )
        if not self.__meta_file.exists():
            raise ValueError(
                "The supplied ' + _META_DATA_CATEGORY + ' file does not exist"
            )

        data_pattern = f"{_V4_VERSION}_{parts.group(_TICKET_INDEX)}_{_DATA_CATEGORY}_*"
        data_files = list(parent.glob(data_pattern))
        if 0 == len(data_files):
            raise ValueError("The supplied ' + _DATA_CATEGORY + ' file does not exist")
        if 1 != len(data_files):
            raise ValueError("Multiple ' + _DATA_CATEGORY + ' files exist")
        self.__payload = data_files[0]
        self.__uid = os.getuid()
        self.__canonical_path: Optional[Path] = None

    def canonical_path(self) -> Path:
        """
        Returns the canonical path for this bundle's payload.
        """
        if None is self.__canonical_path:
            tree = ET.parse(self.__meta_file)
            canonical_element = tree.find("canonical_path")
            if None is canonical_element:
                raise ValueError("No canonical_path in metadata")
            if None is canonical_element.text:
                raise ValueError("Empty canonical_path in metadata")
            self.__canonical_path = Path(canonical_element.text)
        return self.__canonical_path

    def data_name(self) -> str:
        """
        Returns the name of the data file.
        """
        return self.__payload.name

    def done_name(self) -> str:
        """
        Returns the name of the DONE file.
        """
        return self.__done_file.name

    def getmtime(self) -> float:
        """
        Returns the time stamp this object.
        """
        return os.path.getmtime(self.__done_file)

    def metadata_name(self) -> str:
        """
        Returns the name of the metadata file.
        """
        return self.__meta_file.name

    def move(self, destination: Path) -> bool:
        """
        Moves the entire bundle from one directory to another

        Args:
            destination: The directory into which the Bundle should
                be moved.

        Return:
            True is move successful, False otherwise.
        """
        target_payload = destination.joinpath(self.__payload.name)
        target_meta_file = destination.joinpath(self.__meta_file.name)
        target_done_file = destination.joinpath(self.__done_file.name)
        if (
            target_payload.exists()
            or target_meta_file.exists()
            or target_done_file.exists()
        ):
            raise ValueError(
                "At least part of the "
                + self.__bundle
                + " bundle already exists in the destination directory"
            )
        if (
            self.__payload.stat().st_uid == self.__uid
            and self.__meta_file.stat().st_uid == self.__uid
            and self.__done_file.stat().st_uid == self.__uid
        ):
            try:
                # Copies metadata
                logging.debug(
                    'Moving "%s" using %s',
                    self.__bundle,
                    shutil.move.__name__,
                )
                shutil.move(self.__payload, destination)
                shutil.move(self.__meta_file, destination)
                shutil.move(self.__done_file, destination)
            except shutil.Error as move_error:
                raise ValueError(move_error.args[0]) from move_error
        else:
            try:
                # Creates new metadata, i.e. new owner of files
                logging.debug(
                    'Moving "%s" using %s',
                    self.__bundle,
                    nersc_move.__name__,
                )
                nersc_move(self.__payload, destination)
                nersc_move(self.__meta_file, destination)
                nersc_move(self.__done_file, destination)
            except Exception as move_error:
                raise ValueError(move_error.args[0]) from move_error
        return True

    def move_to_canonical(self, root: Path) -> bool:
        """
        Moves the entire bundle to the canonical_path directory.

        Args:
            destination: The directory at which the canonical_path
                starts.

        Return:
            True is move successful, False otherwise.
        """
        canonical = self.canonical_path()
        parking_path = root.joinpath(canonical)
        parking_directory = parking_path.parent
        parking_directory.mkdir(parents=True, exist_ok=True)
        result = self.move(parking_directory)
        bundle_data = parking_directory.joinpath(self.__payload.name)
        parked_data = parking_directory.joinpath(canonical.name)
        bundle_data.rename(parked_data)
        return result

    def name(self) -> str:
        """
        Returns the name of this object.

        Returns:
            The name of this object.
        """
        return self.__bundle


def _report_skipped(reason: str, count: int):
    """
    Outputs a warning about skipped bundles.
    """
    if 1 == count:
        is_or_are = "is"
        plural = ""
    else:
        is_or_are = "are"
        plural = "s"
    logging.warning(
        "There %s %i %s bundle%s in the source directory",
        is_or_are,
        count,
        reason,
        plural,
    )


def find_bundles(directory: Path, ignore: Optional[List[Bundle]]) -> List[Bundle]:
    """
    Returns the list of Bundles in the specified directory.

    Args:
        directory: the directory in which to search for bundles.

    Returns:
        the list of Bundles found.
    """
    ignore_bundles = []
    if None is not ignore:
        for bundle in ignore:
            ignore_bundles.append(bundle.done_name())
    done_files = list(directory.glob(_DONE_FILE_PATTERN))
    result = []
    ignored = 0
    corrupt = 0
    for done_file in done_files:
        if done_file.name in ignore_bundles:
            ignored += 1
        else:
            try:
                result.append(Bundle(done_file))
            except ValueError:
                corrupt += 1
    if 0 != ignored:
        _report_skipped("ignored", ignored)
    if 0 != corrupt:
        _report_skipped("corrupt", corrupt)
    result.sort(key=_getmtime)
    return result


def _getmtime(bundle: Bundle) -> float:
    """
    Returns the time stamp of the supplied Bundle.

    Args:
        destination: The Bundle whose time stamp should be returned.

    Returns:
        The time stamp of the supplied Bundle.
    """
    return bundle.getmtime()
