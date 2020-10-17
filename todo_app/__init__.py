from . import exceptions
from .todo import Todo
from .cli import TodoMenuComponent, TodoEditorComponent
from pyconsoleapp import ConsoleApp

# Create the main app instance
app = ConsoleApp('Todo App')

# Configure some todo_app routes;
app.add_root_route('todos', TodoMenuComponent)
app.add_route('todos.edit', TodoEditorComponent)

# Run the app;
app.run()
