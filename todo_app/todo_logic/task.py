"""Module containing Task class definition."""

from datetime import datetime
from typing import override
from uuid import uuid4

from .task_dict import TaskDict


class Task:
    """Class representing a task with properties."""

    def __init__(  # noqa: PLR0913 (There are actually 5 args)
        self,
        name: str,
        *,
        description: str | None = None,
        due_date: datetime | None = None,
        task_id: str | None = None,
        is_complete: bool = False,
    ) -> None:
        """Initialize the Task instance with provided attributes.

        :param name: The name of the task.
        :param description: The description of the task, defaults to None
        :param due_date: The due date of the task, defaults to None
        :param task_id: The unique identifier of the task, defaults to None
        :param is_complete: The completion status of the task, defaults to False
        """
        self._name: str
        self._description: str | None
        self._due_date: datetime | None
        self._is_complete: bool
        self._task_id: str = task_id if task_id else str(uuid4())

        self.name = name
        self.description = description
        self.due_date = due_date
        self.is_complete = is_complete

    @classmethod
    def from_dict(cls, adict: TaskDict) -> "Task":
        """Create a Task instance from a dictionary.

        :param adict: Input dictionary to create the Task instance.

        :return: A new Task instance created from the input dictionary.
        """
        return cls(**adict)

    def to_dict(self) -> TaskDict:
        """Convert the Task instance to a dictionary.

        :return: A dictionary representation of the Task instance.
        """
        return {
            "name": self._name,
            "description": self._description,
            "due_date": self._due_date,
            "task_id": self._task_id,
            "is_complete": self._is_complete,
        }

    @property
    def task_id(self) -> str:
        """Get the task id of the task.

        :return: The task id of the task.
        """
        return self._task_id

    @property
    def name(self) -> str:
        """Get the name of the task.

        :return: The name of the task.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the task.

        :param value: The new name for the task.

        :raises ValueError: If the name is an empty string.
        """
        value = value.strip()
        if not value:
            msg = "The name of the task cannot be an empty string."
            raise ValueError(msg)
        self._name = str(value)

    @property
    def description(self) -> str | None:
        """Get the description of the task.

        :return: The description of the task, or None if not available.
        """
        return self._description

    @description.setter
    def description(self, value: str | None) -> None:
        """Set the description of the task.

        :param value: The new description for the task, or None if not available.

        :raises ValueError: If the description is an empty string.
        """
        if value is not None:
            value = value.strip()
            if not value:
                msg = "The description of the task cannot be an empty string."
                raise ValueError(msg)
        self._description = value

    @property
    def due_date(self) -> datetime | None:
        """Get the due date of the task.

        :return: The due date of the task, or None if not set.
        """
        return self._due_date

    @due_date.setter
    def due_date(self, value: datetime | None) -> None:
        """Set the due date of the task.

        :param value: The new due date for the task.
        """
        self._due_date = value

    @property
    def is_complete(self) -> bool:
        """Get the completion status of the task.

        :return: True if the task is complete, False otherwise.
        """
        return self._is_complete

    @is_complete.setter
    def is_complete(self, value: bool) -> None:
        """Set the completion status of the task.

        :param value: The new completion status for the task.
        """
        self._is_complete = bool(value)

    @override
    def __repr__(self) -> str:
        """Return a string representation of the Task instance.

        :return: String representation of the Task instance.
        """
        description = f"'{self.description}'" if self.description else None
        return (
            f"<Task(name='{self.name}', "
            f"description={description}, "
            f"due_date={self.due_date}, "
            f"is_complete={self.is_complete}, "
            f"task_id={self.task_id})>"
        )

    @override
    def __eq__(self, value: object) -> bool:
        """Override the equality comparison method.

        :param value: Another object to compare with.
        :return: True if two objects have the same task_id, else False.
        """
        if not isinstance(value, type(self)):
            return False
        return self.task_id == value.task_id

    @override
    def __ne__(self, value: object) -> bool:
        """Override the inequality comparison method.

        :param value: Another object to compare with.
        :return: True if two objects do not have the same task_id, else False.
        """
        return not self.__eq__(value)

    @override
    def __hash__(self) -> int:
        """Override the hashing method.

        :return: Hash value based on the task_id of the object.
        """
        return hash(self.task_id)
