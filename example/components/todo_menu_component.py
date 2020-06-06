from example.todo_service import todos
from textwrap import fill

from pyconsoleapp import ConsoleAppComponent, configs, parse_tools
from example import todo_service

_TEMPLATE = '''TODO's:
{hr}
{todos}
{hr}
(a)  -- Add a todo.
(r*) -- Remove todo number *.
(e*) -- Edit todo number *.
'''


def format_todo(number: int, todo: str) -> str:
    return '{number}. {todo}'.format(
        number=number+1,
        todo=fill(todo, configs.terminal_width_chars) + '\n\n')


class TodoMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        # Configure fixed option responses;
        self.set_option_response('a', self.on_add_todo)

    def print(self):
        # Build the todo list;
        if not len(todo_service.todos):
            todos = "No TODO's added yet."
        else:
            todos = ''
            for i,todo in enumerate(todo_service.todos):
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
        # Try and parse the response into a letter and int;
        try:
            letter, todo_num = parse_tools.parse_letter_and_integer(raw_response)
        except parse_tools.LetterIntegerParseError:
            return # Do nothing if input was invalid.
        # Check the integer refers to a todo;
        if todo_num > len(todo_service.todos) or todo_num < 1:
            # Just return, it can't refer to any on the list;
            return
        # If the user is deleting;
        if letter == 'r':
            todo_service.todos.pop(todo_num-1)
        # If the user is editing;
        elif letter == 'e':
            # Select the todo number;
            todo_service.current_todo_index = todo_num-1
            # Redirect to the editor;
            self.app.goto('todos.edit')
