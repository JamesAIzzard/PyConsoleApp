from . import exceptions, cli
from .todo import Todo
from pyconsoleapp import ConsoleApp

# Create the main app instance
app = ConsoleApp('Todo App')

# Configure some todo_app routes;
app.configure(routes={
    'todos': cli.TodoMenuComponent,
    'todos.edit': cli.TodoEditorComponent
})
# Configure the route to start with;
app.current_route = 'todos'e
