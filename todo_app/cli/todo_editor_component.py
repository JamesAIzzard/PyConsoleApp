from typing import Optional, TYPE_CHECKING

from pyconsoleapp import Component, PrimaryArg, OptionalArg
from pyconsoleapp.builtin_components import StandardPageComponent
from todo_app import cli, service

if TYPE_CHECKING:
    from todo_app.todo import Todo


class TodoEditorComponent(Component):
    """Component to edit the specified todo_."""
    _template = '''
-save \u2502 -> Save the todo.

Update the todo and press enter:
'''

    def __init__(self, **kwds):
        super().__init__(**kwds)

        self.configure(responders=[
            self.configure_responder(self._on_enter, args=[
                PrimaryArg(name='todo_text', accepts_value=True, markers=None),
                PrimaryArg(name='today_flag', accepts_value=False, markers=['--today', '--t']),
                OptionalArg(name='importance_score', accepts_value=True, markers=['--importance', '--i'],
                            validators=[cli.service.validate_importance_score], default_value=1)]),
            self.configure_responder(self._on_save, args=[
                PrimaryArg(name='save', accepts_value=False, markers=['-save'])]
                                     )
        ])
        self.configure(get_prefill=self._get_todo_text)

        self._todo: Optional['Todo'] = None

        self._page_component = self.use_component(StandardPageComponent)
        self._page_component.configure(page_title='Todo Editor')

    def printer(self, **kwds) -> str:
        return self._page_component.printer(page_content=self._template)

    def _get_todo_text(self) -> str:
        """Returns the text from the current todo_."""
        return self._todo.text

    def _on_enter(self, todo_text: str, today_flag: bool, importance_score: int = 1):
        """Handler for when user presses enter."""
        self._todo.saved = False
        self._todo.text = todo_text
        self._todo.today = today_flag
        self._todo.importance = importance_score
        self.app.go_to('todos')

    def _on_save(self) -> None:
        """Saves the _todo."""
        service.save_todo(self._todo)

    def configure(self, todo: Optional['Todo'] = None, **kwds) -> None:
        """Places the todo_ instance on the editor."""
        if todo is not None:
            self._todo = todo
        super().configure(**kwds)
