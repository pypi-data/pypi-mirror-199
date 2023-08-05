"""Define the FileDropper class"""

from typing import Any, List, Optional, Tuple

import os
from pathlib import Path
import shutil

from drip import Dropper, utils

_CONFIG_STRINGS = ["source", "destination"]
_SOURCE_INDEX = 0
_DESTINATION_INDEX = 1
_CONFIG_INTEGERS = ["threshold"]
_THRESHOLD_INDEX = 0

_DEFAULT_THRESHOLD = 8


class FileDropper(Dropper):
    """
    This class provides the concrete implementation use by a Feeder
    instance to copy files from one directory to another.
    """

    def __init__(self, config_file: str, section: str):
        """
        Creates an instance of this class.

        Arg:
            config_file: the name of the file containing the
                configuration information.
            threshold: the maximum number of files allowed in the
                destination directory.
        """

        config = utils.read_config(
            config_file, section, integers=_CONFIG_INTEGERS, strings=_CONFIG_STRINGS
        )
        drip_source = os.getenv("FILE_DRIP_SOURCE")
        if None is drip_source:
            drip_source = str(config[_CONFIG_STRINGS[_SOURCE_INDEX]])
        if None is drip_source:
            raise ValueError(
                "source must be defined in configuration file,"
                + " or envar FILE_DRIP_SOURCE set"
            )
        source = Path(drip_source)
        if not source.exists():
            raise ValueError(f"{source.resolve()} does not exist!")
        self.__src = source

        drip_destination = os.getenv("FILE_DRIP_DESTINATION")
        if None is drip_destination:
            drip_destination = str(config[_CONFIG_STRINGS[_DESTINATION_INDEX]])
        if None is drip_destination:
            raise ValueError(
                "destination must be defined in configuration file,"
                + " or envar FILE_DRIP_DESTINATION set"
            )
        destination = Path(drip_destination)
        if not destination.exists():
            raise ValueError(f"{destination.resolve()} does not exist!")
        self.__dst = destination

        drip_threshold = os.getenv("FILE_DRIP_THRESHOLD")
        if None is drip_threshold:
            config_threshold = config[_CONFIG_INTEGERS[_THRESHOLD_INDEX]]
            if None is config_threshold:
                threshold_to_use = _DEFAULT_THRESHOLD
            else:
                threshold_to_use = int(config_threshold)
                if None is threshold_to_use:
                    threshold_to_use = _DEFAULT_THRESHOLD
            self.__threshold = threshold_to_use
        else:
            self.__threshold = int(drip_threshold)

    def after_dropping(self) -> None:
        """
        Called after a set of `drop` calls.
        """

    def assess_condition(self) -> Tuple[int, str]:
        """
        Assess whether a drip should be executed or not.

        Return:
            maximum number if items that can be dropped and explanation
                of any limitations.
        """
        count = len(os.listdir(self.__dst))
        if 1 == count:
            multiple = ""
            plural = ""
        else:
            multiple = "some of "
            plural = "s"
        if count >= self.__threshold:
            return (
                0,
                f"{multiple}the {count} file{plural} in the target directory to be handled",
            )
        return self.__threshold - count, ""

    def before_dropping(self, count: int) -> None:
        """
        Called before a set of `drop` calls.

        Args:
            count: the number of `drop` calls that will be made in
                the set.
        """

    def drop(self, item) -> bool:
        """
        "Drops" the supplied item, i.e. acts on that item.

        Args:
            item: the item to be dropped.

        Return:
            True if the drop succeeded, false otherwise.
        """
        destination = shutil.move(item, self.__dst)
        return None is not destination

    def fill_cache(self, ignore: Optional[List[Any]] = None) -> List[Any]:
        """
        Fills internal list of items to be dropped.

        Args:
            ignore: A list of item to ignore when filling the
                internal list.
        """
        result = []
        for file in os.listdir(self.__src):
            result.append(self.__src.joinpath(file))
        result.sort(key=os.path.getmtime)
        return result
