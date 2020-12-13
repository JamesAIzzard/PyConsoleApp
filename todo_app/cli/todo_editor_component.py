import copy
from typing import Optional, Callable, TYPE_CHECKING

from pyconsoleapp import Component, Responder, ResponderArg
from pyconsoleapp.builtin_components import StandardPageComponent
from todo_app import cli, service

if TYPE_CHECKING:
    from pyconsoleapp.builtin_components import HeaderComponent
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

    def __init__(self, nav_on_return: Callable[[], None], header_component: 'HeaderComponent', **kwds):
        super().__init__(**kwds)

        self._original_todo: Optional['Todo'] = None
        self._updated_todo: Optional['Todo'] = None
        self._nav_on_return = nav_on_return
        self._save_check_component = cli.TodoSaveCheckComponent(todo_has_changed=self._todo_has_changed,
                                                                save=self._save_changes)
        self._page_component = self.use_component(StandardPageComponent(header_component=header_component))

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

        self._page_component.configure(page_title='Todo Editor')
        self.configure(get_prefill=self._get_todo_text)

    def printer(self, **kwds) -> str:
        return self._page_component.printer(page_content=self._template)

    def _get_todo_text(self) -> str:
        """Returns the text from the current todo_."""
        return self._updated_todo.text

    def _todo_has_changed(self) -> bool:
        return not self._original_todo == self._updated_todo

    def _save_changes(self) -> None:
        service.save_todo(self._original_todo, self._updated_todo)

    def _on_enter(self, todo_text: str, today: bool, importance_score: int, save: bool):
        """Handler for when user presses enter."""
        self._updated_todo.saved = False
        self._updated_todo.text = todo_text
        self._updated_todo.today = today
        self._updated_todo.importance = importance_score
        if save is True and self._todo_has_changed:
            service.save_todo(self._original_todo, self._updated_todo)
        self._nav_on_return()

    def _on_save(self) -> None:
        """Saves the _todo."""
        if self._todo_has_changed:
            service.save_todo(self._original_todo, self._updated_todo)

    def configure(self, todo: Optional['Todo'] = None, **kwds) -> None:
        """Configures."""
        if todo is not None:
            self._original_todo = todo
            self._updated_todo = copy.deepcopy(todo)
        super().configure(**kwds)
        self._page_component.configure(**kwds)
        self._save_check_component.configure(**kwds)
