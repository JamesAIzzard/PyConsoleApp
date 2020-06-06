from pyconsoleapp.console_app import ConsoleApp
from pyconsoleapp import ConsoleAppComponent
from example import todo_service

_TEMPLATE = 'Enter a TODO and press (enter):\n'

class TodoEditorComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)

    def print(self):
        output = self.app.fetch_component('standard_page_component').print(_TEMPLATE)
        # If we are editing a todo;
        if not todo_service.current_todo_index == None:
            return output, todo_service.todos[todo_service.current_todo_index]
        else:
            return output

    def dynamic_response(self, raw_response: str) -> None:
        # Append the todo to the list;
        todo_service.todos.append(raw_response)
        # Redirect back to the main menu;
        self.app.goto('todos')