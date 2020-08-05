from textwrap import fill
from typing import cast, TYPE_CHECKING

import pyconsoleapp as pcap

from example import todo_service, todo

if TYPE_CHECKING:
    from example.components.todo_editor_component import TodoEditorComponent

_template = '''{todos}

-add, -a         [todo]       -> Add a todo.
    --today                   -> Flags as important.
    --importance [level: 1-3] -> Encodes todo as secret.
-remove, -r      [number]     -> Remove a todo.
-edit, -e        [number]     -> Edit a todo.
'''

def format_todo(number: int, todo: 'todo.Todo') -> str:
    return '{number}. {todo_text}'.format(
        number=pcap.styles.weight(str(number), 'bright'),
        todo_text=fill(todo.text, pcap.configs.terminal_width_chars) + '\n\n')


class TodoMenuComponent(pcap.ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.todo_service = todo_service.TodoService()
        # Configure print_function;
        self.configure_printer(self.print_view)
        # Configure response behaviors;
        self.configure_responder(self.add_todo, args=[
            self.configure_primary_arg(name='todo', markers=['-add', '-a']),
            self.configure_option_arg('today', markers=['--today', '--t']),
            self.configure_option_arg('importance', markers=['--importance', '--i'], default_value=1, 
                validators=[pcap.builtin_validators.validate_integer, todo_service.validate_importance_score])  
        ])   
        self.configure_responder(self.remove_todo, args=[
            self.configure_primary_arg('todo_num', markers=['-remove', '-r'], 
                validators=[self._validate_todo_num])
        ])
        self.configure_responder(self.edit_todo, args=[
            self.configure_primary_arg('todo_num', markers=['-edit', '-e'],
                validators=[self._validate_todo_num])
        ])

    def print_view(self):
        # Build the todo list;
        if not len(self.todo_service.todos):
            todos_menu = pcap.styles.fore("No TODO's added yet.", 'blue')
        else:
            todos_menu = ''
            for i, todo in enumerate(self.todo_service.todos):
                todos_menu = todos_menu + format_todo(i+1, todo)

        # Build the main page detail;
        output = _template.format(
            hr=self.app.fetch_component('single_hr_component').print(),
            todos=todos_menu
        )

        # Return in the standard page;
        return self.app.fetch_component('standard_page_component').print(
            page_title="TODOs",
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
