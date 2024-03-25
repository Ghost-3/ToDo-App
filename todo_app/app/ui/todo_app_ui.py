from typing import override

from flet import (
    Column,
    FloatingActionButton,
    Row,
    Tab,
    Tabs,
    TextField,
    UserControl,
    icons,
)


class TodoAppUi(UserControl):
    def __init__(self) -> None:
        super().__init__()  # type: ignore[reportUnknownMemberType] (Bad library typing)
        self.new_task_field = TextField(hint_text="Whats needs to be done?", expand=True, autofocus=True)
        self.add_task_button = FloatingActionButton(icon=icons.ADD)
        self.task_list = Column()

        self.filter = Tabs(
            selected_index=0,
            tabs=[
                Tab(text="all"),
                Tab(text="active"),
                Tab(text="completed"),
            ],
        )

    @override
    def build(self) -> Column:  # type: ignore[reportIncompatibleMethodOverride] (Bad library typing)
        """Build the UI layout for the component.

        :return: The column layout with UI controls.
        """
        new_task_row = Row(
            controls=[
                self.new_task_field,
                self.add_task_button,
            ],
        )

        task_list_column = Column(
            spacing=25,
            controls=[
                self.filter,
                self.task_list,
            ],
        )

        return Column(
            width=600,
            controls=[
                new_task_row,
                task_list_column,
            ],
        )
