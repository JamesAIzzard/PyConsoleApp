from typing import Dict, Callable, TYPE_CHECKING

from pyconsoleapp import Component, Responder, ResponderArg, validators, utils, ResponseValidationError, styles, builtin_components
from pyconsoleapp.builtin_components import StandardPageComponent
from todo_app import service, app

if TYPE_CHECKING:
    from todo_app import Todo
    from todo_app.cli import TodoEditorComponent, TodoDashComponent


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

    def __init__(self, dash_component: 'TodoDashComponent',
                 editor_component: 'TodoEditorComponent',
                 nav_to_editor: Callable[[], None],
                 page_component: 'StandardPageComponent', **kwds):
        super().__init__(**kwds)
        self.configure(responders=[
            Responder(self._on_add_todo, args=[
                ResponderArg(name='todo_text', accepts_value=True, markers=['-add', '-a']),
                ResponderArg(name='today_flag', accepts_value=False, markers=['--today', '--t'], optional=True),
                ResponderArg(name='importance_score', accepts_value=True, markers=['--importance', '--i'],
                             validators=[validators.validate_integer, service.validate_importance_score],
                             default_value=1, optional=True)
            ]),
            Responder(self._on_remove_todo, args=[
                ResponderArg(name='todo_number', accepts_value=True, markers=['-remove', '-r'],
                             validators=[self._validate_todo_num])
            ]),
            Responder(self._on_edit_todo, args=[
                ResponderArg(name='todo_number', accepts_value=True, markers=['-edit', '-e'],
                             validators=[self._validate_todo_num])
            ]),
            Responder(self._on_show_dash, args=None)
        ])

        self._todo_num_map: Dict[int, 'Todo'] = {}

        self._dash_component = self.delegate_state('dash', dash_component)
        self._dash_component.configure(on_back=self.get_state_changer('main'))

        self._editor_component = editor_component
        self._nav_to_editor = nav_to_editor
        self._page_component = self.use_component(page_component)
        self._page_component.configure(page_title='Todo List')

    def on_load(self) -> None:
        self._todo_num_map = utils.make_numbered_map(service.todos)

    def printer(self):
        return self._page_component.printer(page_content=self._template.format(
            todos=self._todo_list_view,
            single_hr=self.single_hr))

    @property
    def _todo_list_view(self) -> str:
        """Returns an enumerated summary of all current _todo's"""
        view = ''
        if service.count_todos() == 0:
            return 'No todo\'s to show yet.'
        else:
            for num, todo in self._todo_num_map.items():
                # Make the text red if today;
                if todo.today:
                    text = styles.fore(todo.text, 'red')
                else:
                    text = todo.text
                view = view + utils.wrap_text('{number:<3} {todo_text}'.format(
                    number=styles.weight(str(num), 'bright') + '.',
                    todo_text=text)) + '\n'
            return view

    def _validate_todo_num(self, value) -> int:
        """Raises ResponseValidationError if number is invalid. Otherwise returns number as int."""
        value = validators.validate_integer(value)
        if value > len(self._todo_num_map):
            raise ResponseValidationError('Input must be a number corresponding to a todo.')
        return value

    @staticmethod
    def _on_add_todo(todo_text: str, today_flag: bool, importance_score: int) -> None:
        """Handler function for when a todo_ is added."""
        service.add_todo(text=todo_text, today=today_flag, importance=importance_score)

    @staticmethod
    def _on_remove_todo(todo_number: int) -> None:
        """Handler function for when a todo_ is removed."""
        service.remove_todo(todo_num=todo_number)

    def _on_edit_todo(self, todo_number: int) -> None:
        """Handler function for when a todo_ is edited."""
        t = service.fetch_todo(todo_number)

        def return_from_edit():
            app.go_to('todos')

        self._editor_component.configure(todo=t, enable_save_check=True, nav_on_return=return_from_edit)
        self._nav_to_editor()

    def _on_show_dash(self) -> None:
        """Switches to dash view state."""
        self.current_state = 'dash'
        # Reconfigure the back button to change the state back to main.
        self._page_component.configure(custom_back=self.get_state_changer('main'))
