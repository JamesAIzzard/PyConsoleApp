from typing import Optional, Callable, TYPE_CHECKING

from pyconsoleapp import Component, Responder, ResponderArg
from pyconsoleapp.builtin_components import StandardPageComponent
from todo_app import cli, service

if TYPE_CHECKING:
    from todo_app.todo import Todo
    from todo_app.cli import TodoSaveCheckComponent


class TodoEditorComponent(Component):
    """Component to edit the specified todo_."""
    _template = u'''
[todo text]
    --today                   \u2502 -> Mark the todo as 'complete today'.
    --importance [level: 1-3] \u2502 -> Give the todo an importance rating.
    --save                    \u2502 -> Save the todo.

Update the todo and press enter:
'''

    def __init__(self, standard_page_component: 'StandardPageComponent',
                 save_check_component: 'TodoSaveCheckComponent',
                 nav_on_return: Callable[[], None] = None, **kwds):
        super().__init__(**kwds)

        self.configure(responders=[
            Responder(self._on_enter, args=[
                ResponderArg(name='todo_text', accepts_value=True, markers=None),
                ResponderArg(name='today', accepts_value=False, markers=['--today'], optional=True),
                ResponderArg(name='importance_score', accepts_value=True, markers=['--importance'],
                             validators=[cli.service.validate_importance_score], default_value=1,
                             optional=True),
                ResponderArg(name='save', accepts_value=False, markers=['--save'], optional=True)
            ]),
        ])
        self.configure(get_prefill=self._get_todo_text)

        self._todo: Optional['Todo'] = None
        self._nav_on_return = nav_on_return
        self._save_check_component = save_check_component
        self._page_component = self.use_component(standard_page_component)
        self._page_component.configure(page_title='Todo Editor')

    def printer(self, **kwds) -> str:
        return self._page_component.printer(page_content=self._template)

    def _get_todo_text(self) -> str:
        """Returns the text from the current todo_."""
        return self._todo.text

    def _on_enter(self, todo_text: str, today: bool, importance_score: int, save: bool):
        """Handler for when user presses enter."""
        self._todo.saved = False
        self._todo.text = todo_text
        self._todo.today = today
        self._todo.importance = importance_score
        if save is True:
            service.save_todo(self._todo)
        self._nav_on_return()

    def _on_save(self) -> None:
        """Saves the _todo."""
        service.save_todo(self._todo)

    def configure(self, todo: Optional['Todo'] = None,
                  nav_on_return: Optional[Callable[[], None]] = None,
                  enable_save_check: Optional[bool] = None,
                  **kwds) -> None:
        """Places the todo_ instance on the editor."""
        if todo is not None:
            self._todo = todo
        if nav_on_return is not None:
            self._nav_on_return = nav_on_return
        if enable_save_check is not None:
            self._save_check_component.configure(enable=enable_save_check)
        super().configure(**kwds)
