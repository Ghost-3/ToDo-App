"""Module containing TaskEvent Enum for task events."""

from enum import Enum


class TaskEvent(Enum):
    """Enumeration of task events."""

    SWITCH_COMPLETE = "switch_complete"
    RENAME = "rename"
    DELETE = "delete"
