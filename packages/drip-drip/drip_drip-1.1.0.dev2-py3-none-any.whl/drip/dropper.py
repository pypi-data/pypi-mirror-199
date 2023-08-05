"""Define the Dropper class"""

from typing import Any, List, Optional, Tuple


class Dropper:
    """
    This class provides the concrete implementation use by a Feeder
    instance to execute a particular type of drip-feed.
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
        return (0, "")

    def before_dropping(self, count: int) -> None:
        """
        Called before a set of `drop` calls.

        Args:
            count: the number of `drop` calls that will be made in
                the set.
        """

    def drop(self, item: Any) -> bool:  # pylint: disable=unused-argument
        """
        "Drops" the supplied item, i.e. acts on that item.

        Arg:
            item: the item to be dropped.

        Return:
            True if the drop succeeded, false otherwise.
        """
        return False

    def fill_cache(  # pylint: disable=unused-argument
        self, ignore: Optional[List[Any]] = None
    ) -> List[Any]:
        """
        Fills internal list of items to be dropped.

        Args:
            ignore: A list of item to ignore when filling the
                internal list.
        """
        return []
