"""Module contains the Task class and related attributes for creating and managing tasks."""

from collections.abc import Callable
from datetime import date, datetime, time
from typing import override

from flet import (
    ControlEvent,
    icons,
)

from todo_app.todo_logic.task import Task

from .task_event import TaskEvent
from .ui.task_ui import TaskUi


class TaskControl(TaskUi):
    """Represents a task for managing to-do items."""

    def __init__(
        self,
        task: Task,
        on_task_event: Callable[[TaskEvent, "TaskControl"], None],
    ) -> None:
        """Initialize a Task object with the given parameters.

        :param task_name: The name of the task.
        :param on_task_event: A callback function for handling task events.
        """
        super().__init__()
        self._task = task
        self._on_task_event = on_task_event

        # Display elements
        self._display_task.label = self._task.name
        self._display_task.value = self._task.is_complete
        self._display_task.on_change = self._on_status_change
        self._edit_task_btn.on_click = self._on_edit_click
        self._delete_task_btn.on_click = self._on_delete_click
        self._description_indicator.visible = self._task.description is not None
        self._date_indicator_text.value = due_date.isoformat() if (due_date := self._task.due_date) else None
        self._date_indicator.visible = self._task.due_date is not None
        self._time_indicator_text.value = due_time.isoformat()[:5] if (due_time := self._task.due_time) else None
        self._time_indicator.visible = self._task.due_time is not None

        # Edit elements
        self._date_picker.on_change = self._on_pick_date
        self._time_picker.on_change = self._on_pick_time
        self._date_picker_btn.on_click = self._on_open_date_picker
        self._time_picker_btn.on_click = self._on_open_time_picker
        self._save_btn.on_click = self._on_save_click

    @property
    def task(self) -> Task:
        """Returns the Task instance responsible for managing the task logic.

        :return: The Task instance handling the task logic.
        """
        return self._task

    @override
    def update(self) -> None:
        """Update the task information and indicators.

        This method updates the description, date, and time of the task.
        """
        self._description_indicator.visible = self._task.description is not None

        self._update_date()
        self._update_time()

        super().update()

    def _update_date(self) -> None:
        """Update the date information for the task.

        This method updates the due date text, icon, and visibility indicator.
        """
        if due_date := self._task.due_date:
            self._date_picker_btn.text = due_date.isoformat()
            self._date_picker_btn.icon = icons.CANCEL_OUTLINED
            self._date_indicator_text.value = due_date.isoformat()
            self._date_indicator.visible = True
        else:
            self._date_picker_btn.text = "Due date"
            self._date_picker_btn.icon = icons.CALENDAR_MONTH_OUTLINED
            self._date_indicator.visible = False

    def _update_time(self) -> None:
        """Update the time information for the task.

        This method updates the due time text, icon, and visibility indicator.
        """
        if due_time := self._task.due_time:
            self._time_picker_btn.text = due_time.isoformat()[:5]
            self._time_picker_btn.icon = icons.CANCEL_OUTLINED
            self._time_indicator_text.value = due_time.isoformat()[:5]
            self._time_indicator.visible = True
        else:
            self._time_picker_btn.text = "Due time"
            self._time_picker_btn.icon = icons.ACCESS_TIME
            self._time_indicator.visible = False

    def _on_edit_click(self, _: ControlEvent) -> None:
        """Handle edit button click event.

        :param _: The control event object.
        """
        self._edit_name_field.value = self._task.name
        self._edit_name_field.focus()
        if (description := self._task.description) is not None:
            self._edit_description_field.value = description
        self._display_view.visible = False
        self._edit_view.visible = True
        self.update()

    def _on_open_date_picker(self, _: ControlEvent) -> None:
        """Handle pick date button click.

        If the date is not set, it calls date picker; otherwise, the set date is cleared.

        :param _: The control event object.
        """
        if not self._task.due_date:
            self._date_picker.pick_date()
        else:
            self._task.due_date = None
        self.update()

    def _on_open_time_picker(self, _: ControlEvent) -> None:
        """Handle pick time button click.

        If the time is not set, it calls time picker; otherwise, the set time is cleared.

        :param _: The control event object.
        """
        if not self._task.due_time:
            self._time_picker.pick_time()
        else:
            self._task.due_time = None
        self.update()

    def _on_pick_date(self, e: ControlEvent) -> None:
        """Handle pick due date event.

        :param _: The control event object.
        """
        pick_date: date = datetime.fromisoformat(e.data).date()
        self._task.due_date = pick_date
        self.update()

    def _on_pick_time(self, e: ControlEvent) -> None:
        """Handle pick due time event.

        :param _: The control event object.
        """
        due_time = ":".join([x.zfill(2) for x in e.data.split(":")])
        pick_time: time = time.fromisoformat(due_time)
        self._task.due_time = pick_time
        self.update()

    def _on_save_click(self, _: ControlEvent) -> None:
        """Handle save button click event.

        :param _: The control event object.
        """
        if isinstance(name := self._edit_name_field.value, str):
            name = name.strip()
        if not name:
            return

        if isinstance(description := self._edit_description_field.value, str):
            description = description.strip()
        if not description:
            description = None

        self._task.name = name
        self._task.description = description
        self._on_task_event(TaskEvent.MODIFY, self)

        self._display_task.label = name

        self._display_view.visible = True
        self._edit_view.visible = False
        self.update()

    def _on_status_change(self, _: ControlEvent) -> None:
        """Handle status change event.

        :param _: The control event object.
        """
        if (is_complete := self._display_task.value) is not None:
            self._task.is_complete = is_complete
            self._on_task_event(TaskEvent.SWITCH_COMPLETE, self)

    def _on_delete_click(self, _: ControlEvent) -> None:
        """Handle delete button click event.

        :param _: The control event object.
        """
        self._on_task_event(TaskEvent.DELETE, self)
