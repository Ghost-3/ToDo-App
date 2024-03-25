"""Module representing a Todo App user control with task management functionality."""

from typing import override

from flet import (
    Column,
    ControlEvent,
    FloatingActionButton,
    Row,
    Tab,
    Tabs,
    TextField,
    UserControl,
    icons,
)

from todo_app.todo_logic.task import Task
from todo_app.todo_logic.task_manager import TaskManager
from todo_app.utils import Utils

from .filter_status import FilterStatus
from .task_event import TaskEvent
from .task_ui import TaskUi


class TodoApp(UserControl):
    """A class representing a Todo App user control."""

    def __init__(self) -> None:
        """Initialize a new instance of TodoApp."""
        super().__init__()  # type: ignore[reportUnknownMemberType] (Bad library typing)
        self.new_task_field = TextField(hint_text="Whats needs to be done?", expand=True, autofocus=True)
        self.add_task_button = FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked)
        self.task_list = Column()

        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                Tab(text="all"),
                Tab(text="active"),
                Tab(text="completed"),
            ],
        )
        self.task_manager = TaskManager()
        self.load_tasks()

    def load_tasks(self) -> None:
        """Load tasks from a file during initialization.

        This method loads tasks using the TaskManager and creates TaskUi objects for each task to update the UI.
        """
        self.task_manager.load_tasks()
        for task in self.task_manager.tasks:
            task_ui = TaskUi(task, self.on_task_event)
            self.task_list.controls.append(task_ui)

    @override
    def build(self) -> Column:  # type: ignore[reportIncompatibleMethodOverride] (Bad library typing)
        """Build the UI layout for the component.

        :return: The column layout with UI controls.
        """
        return Column(
            width=600,
            controls=[
                Row(
                    controls=[
                        self.new_task_field,
                        self.add_task_button,
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.task_list,
                    ],
                ),
            ],
        )

    @override
    def update(self) -> None:
        """Update the screen with changes based on selected filter status.

        Method checks the filter status and updates the visibility of tasks accordingly.
        """
        if not (tabs := self.filter.tabs):
            return
        filter_index = self.filter.selected_index if self.filter.selected_index else 0
        status = Utils.get_filter_status(
            tabs[filter_index].text,  # type: ignore[reportUnknownMemberType] (Bad library typing)
        )
        for task_ui in self.task_list.controls:
            if not isinstance(task_ui, TaskUi):
                continue
            task_ui.visible = (
                status == FilterStatus.ALL
                or (status == FilterStatus.ACTIVE and task_ui.task.is_complete is False)
                or (status == FilterStatus.COMPLETED and task_ui.task.is_complete)
            )

        super().update()

    def add_clicked(self, _: ControlEvent) -> None:
        """Handle the click event when the add button is clicked.

        :param _: The control event object.
        """
        if not self.new_task_field.value:
            return
        task_ui = TaskUi(
            Task(self.new_task_field.value),
            self.on_task_event,
        )
        if self.task_manager.add_task(task_ui.task):
            self.task_list.controls.append(task_ui)
            self.new_task_field.value = ""
            self.update()

    def on_task_event(self, task_event: TaskEvent, task_ui: TaskUi) -> None:
        """Handle a task event by modifying tasks in the TaskManager and updating the UI.

        :param task_event: The TaskEvent that occurred for the task.
        :param task_ui: The TaskUi object associated with the task.
        """
        task = task_ui.task
        match task_event:
            case TaskEvent.RENAME:
                result = self.task_manager.modify_task(task.task_id, name=task.name)
            case TaskEvent.SWITCH_COMPLETE:
                result = self.task_manager.modify_task(task.task_id, is_complete=task.is_complete)
            case TaskEvent.DELETE:
                result = self.task_manager.delete_task(task.task_id)
                if result:
                    self.task_list.controls.remove(task_ui)
        if result:
            self.update()

    def tabs_changed(self, _: ControlEvent) -> None:
        """Handle the event when filter tab are changed.

        :param _: The control event object.
        """
        self.update()
