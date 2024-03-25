"""Module for creating and running the ToDo application."""

from flet import CrossAxisAlignment, Page, app  # type: ignore[reportUnknownVariableType] (Bad library typing)

from .todo_app import TodoApp


class App:
    """Class representing the main application."""

    @staticmethod
    def main(page: Page) -> None:
        """Set up the main UI page for the ToDo application.

        :param page: The UI page for the application.
        """
        page.title = "ToDo App"
        page.horizontal_alignment = CrossAxisAlignment.CENTER
        page.update()  # type: ignore[reportUnknownMemberType] (Bad library typing)
        page.add(TodoApp())  # type: ignore[reportUnknownMemberType] (Bad library typing)

    def run(self) -> None:
        """Run the main application."""
        _ = app(target=self.main)
