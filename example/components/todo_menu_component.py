from textwrap import fill
from typing import cast, TYPE_CHECKING

import pyconsoleapp as pcap

from example import todo_service, todo

if TYPE_CHECKING:
    from example.components.todo_editor_component import TodoEditorComponent

_home_template = '''{todos}
-add, -a         [todo]       -> Add a todo.
    --today                   -> Flags as important.
    --importance [level: 1-3] -> Encodes todo as secret.
-remove, -r      [number]     -> Remove a todo.
-edit, -e        [number]     -> Edit a todo.
-dash                         -> View todo dashboard.
'''

_dash_template = '''
There are currently {todo_count} todo's.

-home                         -> Back to home.
'''

def format_todo(number: int, todo: 'todo.Todo') -> str:
    # Make the text red if today;
    if todo.today:
        text = pcap.styles.fore(todo.text, 'red')
    else: 
        text=todo.text
    # Build & return the string;
    return '{number}. {todo_text}'.format(
        number=pcap.styles.weight(str(number), 'bright'),
        todo_text=fill(text, pcap.configs.terminal_width_chars) + '\n\n')


class TodoMenuComponent(pcap.ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)

        self.todo_service = todo_service.TodoService()

        self.configure_states(['home', 'dash'])

        # Configure home state;
        self.configure_printer(self.print_home_view, ['home'])
        self.configure_responder(self.add_todo, states=['home'], args=[
            self.configure_std_primary_arg(name='todo', markers=['-add', '-a']),
            self.configure_valueless_option_arg(name='today', markers=['--today', '--t']),
            self.configure_std_option_arg('importance', markers=['--importance', '--i'], default_value=1, 
                validators=[pcap.builtin_validators.validate_integer, todo_service.validate_importance_score])  
        ])   
        self.configure_responder(self.remove_todo, states=['home'], args=[
            self.configure_std_primary_arg('todo_num', markers=['-remove', '-r'], 
                validators=[self.todo_service.validate_todo_num])
        ])
        self.configure_responder(self.edit_todo, states=['home'], args=[
            self.configure_std_primary_arg('todo_num', markers=['-edit', '-e'],
                validators=[self.todo_service.validate_todo_num])
        ])
        self.configure_responder(self.change_state('dash'), states=['home'], args=[
            self.configure_valueless_primary_arg('dash', ['-dash'])
        ])        

        # Configure dashboard state;
        self.configure_printer(self.print_dash_view, ['dash'])
        self.configure_responder(self.change_state('home'), states=['dash'], args=[
            self.configure_valueless_primary_arg('home', ['-home'])
        ])

    def print_home_view(self):
        # Build the todo list;
        if not len(self.todo_service.todos):
            todos_menu = pcap.styles.fore("No TODO's added yet.\n", 'blue')
        else:
            todos_menu = ''
            for i, todo in enumerate(self.todo_service.todos):
                todos_menu = todos_menu + format_todo(i+1, todo)

        # Build the main page detail;
        output = _home_template.format(
            hr=self.app.fetch_component('single_hr_component').print(),
            todos=todos_menu
        )

        # Return in the standard page;
        return self.app.fetch_component('standard_page_component').print(
            page_title="TODOs",
            page_content=output
        )

    def print_dash_view(self):
        output = _dash_template.format(
            todo_count=len(self.todo_service.todos)
        )
        return self.app.fetch_component('standard_page_component').print(
            page_title="Todo Dashboard",
            page_content=output
        )

    def add_todo(self, args) -> None:
        self.todo_service.add_todo(args['todo'], args['today'], args['importance'])

    def remove_todo(self, args) -> None:
        self.todo_service.remove_todo(args['todo_num'])

    def edit_todo(self, args) -> None:
        # Configure the editor component;
        tde = self.app.fetch_component('todo_editor_component')
        tde = cast('TodoEditorComponent', tde)
        tde.subject = self.todo_service.fetch_todo(args['todo_num'])

        # Head to the editor;
        self.app.goto('todos.edit')