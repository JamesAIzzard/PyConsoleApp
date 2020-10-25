from . import exceptions, cli
from .todo import Todo
from pyconsoleapp import ConsoleApp

# Create the main app instance
app = ConsoleApp('Todo App')

# Configure some todo_app routes;
app.configure(routes=[
    RootRoute('todos', cli.TodoMenuComponent),
    Route('todos.edit', cli.TodoEditorComponent)
])
