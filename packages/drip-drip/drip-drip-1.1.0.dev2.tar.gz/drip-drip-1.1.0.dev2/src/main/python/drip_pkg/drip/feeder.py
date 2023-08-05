"""Define the Feeder class"""

from typing import Any, Callable, List, TypeAlias, Union
from types import FrameType

import logging
from pathlib import Path
from signal import Handlers
import signal
from threading import Event
import time

from drip import Dropper

_SigHandler: TypeAlias = Union[
    Callable[[int, FrameType | None], Any], int, Handlers, None
]
Paths = list[Path]


class Feeder:  # pylint: disable=too-many-instance-attributes
    """
    This class manages the drip feeding of a collection of items, where
    "drip feeding" means that when a specified condition is met an
    action is taken on a batch of those items that are then removed from
    that list. While executing the collection new items name be added to
    the collection.
    """

    BATCH_SIZE_DEFAULT: int = 8
    PAUSE_INTERVAL_DEFAULT: int = 30
    REFILL_INTERVAL_DEFAULT: int = 120

    def __init__(
        self,
        dropper: Dropper,
        batch_size: int = BATCH_SIZE_DEFAULT,
        pause_interval: int = PAUSE_INTERVAL_DEFAULT,
        refill_interval: int = REFILL_INTERVAL_DEFAULT,
    ):
        """
        Creates an instance of this class.

        Args:
            dropper_class: the class that will feed the drops while dripping.
            batch_size: the maximum number of drops per drip.
            pause_interval: the number of seconds to wait before checking the condition again.
            refill_interval: the number of seconds to wait after the source is
                                empty before resuming.
        """
        self.__batch_size = batch_size
        self.__cache: List[Any] = []
        self.__dropper = dropper
        self.__ignore: List[Any] = []
        self.__pause_interval = pause_interval
        self.__previous_sigint: _SigHandler = None
        self.__refill_interval = refill_interval
        self.__running = Event()

    def drip(self, pause: bool = False) -> int:
        """
        Runs a single "drip", i.e moves one batch of files from source
        to destination when a specified condition is met.

        Args:
            pause: True if this method should pause before dripping.
        """

        (available, condition) = self.__dropper.assess_condition()
        condition_to_use = None
        if 0 == available and None is not condition:
            condition_to_use = condition + " "
        elif pause or 0 == available:
            condition_to_use = ""
        if None is not condition_to_use:
            logging.info(
                "Waiting %i seconds for %s",
                self.__pause_interval,
                condition_to_use + "before feeding more items",
            )
            self.__running.wait(self.__pause_interval)
            return 0

        cache_size = len(self.__cache)
        if cache_size < self.__batch_size:
            self.__cache = self.__dropper.fill_cache(self.__ignore)
            cache_size = len(self.__cache)
        if 0 == cache_size:
            logging.info(
                "Source of items is empty, waiting for %i seconds",
                self.__refill_interval,
            )
            self.__running.wait(self.__refill_interval)
            return 0

        if 1 == cache_size:
            to_be = "is"
            plural = ""
        else:
            to_be = "are"
            plural = "s"
        logging.info(
            "There %s at least %i item%s waiting to be fed.", to_be, cache_size, plural
        )
        end = min(available, self.__batch_size, cache_size)
        self.__dropper.before_dropping(end)
        count = 0
        t_0 = time.time()
        for item in self.__cache[0:end]:
            dropped = self.__dropper.drop(item)
            if dropped:
                count = count + 1
            else:
                self.__ignore.append(item)
                logging.warning('Item "%s" failed to be dropped', item)
        t_1 = time.time()
        self.__dropper.after_dropping()
        self.__cache = self.__cache[count:]
        if 1 == count:
            plural = ""
        else:
            plural = "s"
        logging.info(
            "Finished moving item%s %i to the destination in %i seconds",
            plural,
            count,
            int(t_1 - t_0 + 0.5),
        )
        return count

    def run(self) -> None:
        """
        Runs a loop to execute the drop-feeding.
        """
        self.__running.clear()
        self.__previous_sigint = signal.signal(signal.SIGINT, self.__stop)
        moved = 0
        while not self.__running.is_set():
            moved = self.drip(0 != moved)

    def __stop(
        self,
        signum,  # pylint: disable=unused-argument
        frame,  # pylint: disable=unused-argument
    ) -> None:
        """
        Signal handler to stop this item from running.
        """
        self.stop()

    def stop(self) -> None:
        """
        Signals that the drip-feeding loop should exit.
        """
        self.__running.set()
        if None is not self.__previous_sigint:
            signal.signal(signal.SIGINT, self.__previous_sigint)
