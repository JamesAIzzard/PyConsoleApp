from typing import Dict, TYPE_CHECKING

from pyconsoleapp import Component, Responder, ResponderArg, validators, utils, ResponseValidationError, styles, \
    builtin_components
from todo_app import cli, service

if TYPE_CHECKING:
    from pyconsoleapp.builtin_components import HeaderComponent
    from todo_app import Todo
    from todo_app.cli import TodoEditorComponent, TodoDashComponent


class TodoMenuComponent(Component):
    _template = u'''{todos}
{single_hr}
-add, -a         [todo_item]  \u2502 -> Add a todo.
    --today                   \u2502 -> Flags as important.
    --importance [level: 1-3] \u2502 -> Describes the importance of a todo.
-remove, -r      [number]     \u2502 -> Remove a todo.
-edit, -e        [number]     \u2502 -> Edit a todo.
(enter)                       \u2502 -> View the dashboard.
{single_hr}
'''

    def __init__(self, header_component: 'HeaderComponent',
                 todo_editor_component: 'TodoEditorComponent',
                 editor_route: str, **kwds):
        super().__init__(**kwds)

        self._todo_num_map: Dict[int, 'Todo'] = {}
        self.dash_nav_component = \
            builtin_components.NavOptionsComponent(
                on_back=self.get_state_changer('main'),
                on_quit=header_component.nav_options_component._on_quit_, # noqa
                get_current_route=header_component.nav_options_component._get_current_route # noqa
            )
        self.dash_nav_component.configure(on_back=self.get_state_changer('main'))
        self.dash_header = \
            builtin_components.HeaderComponent(title_bar_component=header_component.title_bar_component,
                                               nav_options_component=self.dash_nav_component,
                                               message_bar_component=header_component.message_bar_component)
        self.dash_header.configure(on_back=self.get_state_changer('main'))
        self.dash_component = self.delegate_state('dash', cli.TodoDashComponent(header_component=self.dash_header))
        self.editor_component = todo_editor_component
        self._editor_route = editor_route
        self.page_component = self.use_component(
            builtin_components.StandardPageComponent(header_component=header_component,
                                                     page_title='Todo List')
        )

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

    def on_load(self) -> None:
        self._todo_num_map = utils.make_numbered_map(service.todos)

    def printer(self):
        return self.page_component.printer(page_content=self._template.format(
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
        self.editor_component.configure(todo=t)

    def _on_show_dash(self) -> None:
        """Switches to dash view state."""
        self.current_state = 'dash'
