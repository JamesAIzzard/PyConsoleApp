from pyconsoleapp import ConsoleAppComponent
from example import todo_service

_TEMPLATE = 'Enter a TODO and press (enter):\n'

class TodoEditorComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.todo_service = todo_service.TodoService()

    def print(self):
        output = self.app.fetch_component('standard_page_component').print(_TEMPLATE)
        # If we are editing a todo;
        if self.todo_service.editing:
            return output, self.todo_service.selected_todo
        # If we are creating a new todo;
        else:
            return output

    def dynamic_response(self, raw_response: str) -> None:
        # If we are editing a todo;
        if self.todo_service.editing:
            # Update it;
            self.todo_service.todos[self.todo_service.current_todo_index] = raw_response
        # If we are creating a new todo;
        elif not self.todo_service.editing:
            # Append the todo to the list;
            self.todo_service.todos.append(raw_response)
        # Turn off edit mode;
        self.todo_service.editing = False
        # Redirect back to the main menu;
        self.app.goto('todos')