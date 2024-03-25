"""Module containing an Enum for filter status."""

from enum import Enum
from typing import Literal


class FilterStatus(Enum):
    """Enum class representing different filter statuses."""

    ALL = "all"
    ACTIVE = "active"
    COMPLETED = "completed"

    @staticmethod
    def from_str(string: Literal["all", "active", "completed"]) -> "FilterStatus":
        """Return the FilterStatus enum value corresponding to the input string.

        :param string: The input string representing filter status.
        :return: The corresponding FilterStatus enum value.
        """
        match string:
            case "all":
                return FilterStatus.ALL
            case "active":
                return FilterStatus.ACTIVE
            case "completed":
                return FilterStatus.COMPLETED
