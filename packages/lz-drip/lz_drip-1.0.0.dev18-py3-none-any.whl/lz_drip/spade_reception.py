"""Define the FileDropper class"""

from typing import List, Optional, Tuple

import logging

from drip import Dropper

from .bundle import find_bundles, Bundle, _DONE_FILE_PATTERN
from .file_utils import (
    read_config,
    select_source,
    select_destination,
    select_threshold,
)


class SpadeReception(Dropper):
    """
    This class provides the concrete implementation use by a Feeder
    instance to copy SPADE bundles from one directory to another.
    """

    def __init__(self, config_file: str, section: str):
        """
        Creates an instance of this class.

        :param source: the Path to the source directory
        :param destination: the Path to the destination directory
        """
        config = read_config(config_file, section)

        self.__src = select_source(config)
        self.__dst = select_destination(config)
        self.__threshold = select_threshold(config)
        logging.debug("Begin SpadeReception configuration:")
        logging.debug("    %s = %s", "source", self.__src)
        logging.debug("    %s = %s", "destination", self.__dst)
        logging.debug("    %s = %s", "threshold", self.__threshold)
        logging.debug("End SpadeReception configuration:")

    def assess_condition(self) -> Tuple[int, str]:
        """
        Assess whether a drip should be executed or not.

        :return maximum number if items that can be dropped and
        explanation of any limitations.
        """
        count = len(list(self.__dst.glob(_DONE_FILE_PATTERN)))
        if 1 == count:
            multiple = ""
            plural = ""
        else:
            multiple = "some of "
            plural = "s"
        if count >= self.__threshold:
            return (
                0,
                f"{multiple}the {count} bundle{plural} in the target directory to be handled",
            )
        return self.__threshold - count, ""

    def drop(self, item) -> bool:
        """
        "Drops" the supplied item, i.e. acts on that item.
        """
        try:
            return item.move(self.__dst)
        except ValueError as valueerror:
            logging.warning(valueerror.args[0])
            return False

    def fill_cache(self, ignore: Optional[List[Bundle]] = None) -> List[Bundle]:
        """
        Fills internal list of items to be dropped.

        Args:
            ignore: A list of item to ignore when filling the
                internal list.
        """
        return find_bundles(self.__src, ignore)
