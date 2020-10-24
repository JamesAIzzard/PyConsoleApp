from typing import Dict, Callable, Optional, TYPE_CHECKING

from pyconsoleapp import Component, PrimaryArg, OptionalArg, validators, utils, ResponseValidationError
from pyconsoleapp.builtin_components import StandardPageComponent
from todo_app import service, cli

if TYPE_CHECKING:
    from todo_app import Todo


class TodoMenuComponent(Component):
    _template = u'''{todos}
{single_hr}
-add, -a         [todo_item]  \u2502 -> Add a todo_item.
    --today                   \u2502 -> Flags as important.
    --importance [level: 1-3] \u2502 -> Describes the importance of a todo.
-remove, -r      [number]     \u2502 -> Remove a todo_item.
-edit, -e        [number]     \u2502 -> Edit a todo_item.
(enter)                       \u2502 -> View todo_item dashboard.
{single_hr}
'''

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.configure(responders=[
            self.configure_responder(self._on_add_todo, args=[
                PrimaryArg(name='todo_text', accepts_value=True, markers=['-add', '-a']),
                OptionalArg(name='today_flag', accepts_value=False, markers=['--today', '--t']),
                PrimaryArg(name='importance_score', accepts_value=True, markers=['--importance', '--i'],
                           validators=[validators.validate_integer, service.validate_importance_score],
                           default_value=1)]),
            self.configure_responder(self._on_remove_todo, args=[
                PrimaryArg(name='todo_number', accepts_value=True, markers=['-remove', 'r'],
                           validators=[self._validate_todo_num])]),
            self.configure_responder(self._on_edit_todo, args=[
                PrimaryArg(name='todo_number', accepts_value=True, markers=['-edit', '-e'],
                           validators=[self._validate_todo_num])]),
            self.configure_responder(self.get_state_changer('dash'), args=None)
        ])

        self._todo_num_map: Dict[int, 'Todo'] = {}

        self._dash_component = self.delegate_state('dash', TodoDashComponent)
        self._dash_component.configure(on_go_home=self.get_state_changer('main'))
        self._editor_component = self.delegate_state('edit', cli.TodoEditorComponent)
        self._page_component = self.use_component(StandardPageComponent)
        self._page_component.configure(page_title='Todo List')

    def on_load(self) -> None:
        self._todo_num_map = utils.make_numbered_map(service.todos)

    def printer(self):
        return self._page_component.printer(page_content=self._template.format(
            todos=self._todo_list_view,
            single_hr=u'\u2500' * self.app.terminal_width))

    @property
    def _todo_list_view(self) -> str:
        """Returns an enumerated summary of all current _todo's"""
        view = ''
        if service.count_todos() is 0:
            return 'No todo\'s to show yet.'
        else:
            for num, todo in self._todo_num_map.items():
                view = view + '{num:<3} {todo_summary}\n'.format(
                    num=str(num) + '.',
                    todo_summary=utils.truncate_text(todo.text, self.app.terminal_width - 10)
                )
            return view

    def _validate_todo_num(self, value) -> int:
        """Raises ResponseValidationError if number is invalid. Otherwise returns number as int."""
        value = validators.validate_integer(value)
        if value > len(self._todo_num_map):
            raise ResponseValidationError('Input must be a number corresponding to a todo.')
        return value

    @staticmethod
    def _on_add_todo(todo_text: str, today_flag: bool, importance_score: int) -> None:
        service.add_todo(text=todo_text, today=today_flag, importance=importance_score)

    @staticmethod
    def _on_remove_todo(todo_number: int) -> None:
        service.remove_todo(todo_num=todo_number)

    def _on_edit_todo(self, todo_number: int) -> None:
        t = service.fetch_todo(todo_number)
        self._editor_component.configure(todo=t)
        self.app.guard_exit('todos.edit', cli.TodoSaveCheckComponent)
        self.app.go_to('todos.edit')


class TodoDashComponent(Component):
    _template = u'''-home \u2502 -> Back to home.

There are currently {todo_count} todo_item's.
'''

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._on_go_home_: Optional[Callable[[], None]] = None
        self.configure(responders=[
            self.configure_responder(self._on_go_home_, args=[
                PrimaryArg(name='home', accepts_value=False, markers=['-home'])
            ])
        ])

    def printer(self, **kwds) -> str:
        return self._template.format(todo_count=service.count_todos())

    def configure(self, on_go_home: Optional[Callable[[], None]] = None, **kwds) -> None:
        if on_go_home is not None:
            self._on_go_home_ = on_go_home
        super().configure(**kwds)
