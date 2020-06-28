from textwrap import fill

from pyconsoleapp import ConsoleAppComponent, configs, parse_tools, styles
from example import todo_service

_TEMPLATE = '''TODO's:
{hr}
{todos}
{hr}
(-a)   -- Add a todo.
(-r *) -- Remove todo number *.
(-e *) -- Edit todo number *.
'''


def format_todo(number: int, todo: str) -> str:
    return '{number}. {todo}'.format(
        number=styles.weight(str(number+1), 'bright'),
        todo=fill(todo, configs.terminal_width_chars) + '\n\n')


class TodoMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.todo_service = todo_service.TodoService()
        # Configure fixed option responses;
        self.set_option_response('-a', self.on_add_todo)

    def print(self):
        # Build the todo list;
        if not len(self.todo_service.todos):
            todos = styles.fore("No TODO's added yet.", 'blue')
        else:
            todos = ''
            for i,todo in enumerate(self.todo_service.todos):
                todos = todos + format_todo(i, todo)
        # Build the main page detail;
        output = _TEMPLATE.format(
            hr=self.app.fetch_component('single_hr_component').print(),
            todos=todos
        )
        # Return in the standard page;
        return self.app.fetch_component('standard_page_component').print(output)

    def on_add_todo(self):
        self.app.goto('todos.edit')

    def dynamic_response(self, raw_response: str) -> None:
        # Parse into flags and string;
        flags, todo_num = parse_tools.parse_flags_and_text(raw_response)

        # Check the number can be an integer;
        if not todo_num:
            return
        try:
            todo_num = int(todo_num)
        except ValueError:
            return
        # Check the integer refers to a todo;
        if todo_num > len(self.todo_service.todos) or todo_num < 1:
            # Just return, it can't refer to any on the list;
            return

        # If the user is deleting;
        if flags == ['-r']:
            self.todo_service.todos.pop(todo_num-1)

        # If the user is editing;
        elif flags == ['-e']:
            # Set the todo index and switch to editing;
            self.todo_service.current_todo_index = todo_num-1
            self.todo_service.editing = True
            # Redirect to the editor;
            self.app.goto('todos.edit')
