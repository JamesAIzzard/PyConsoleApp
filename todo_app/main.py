from pyconsoleapp import ConsoleApp

from todo_app import cli

# Create the app instance;
app = ConsoleApp('Example Todo App')

# Instantiate the components;
todo_menu_component = cli.TodoMenuComponent()
todo_editor_component = cli.TodoEditorComponent()

# Bind the components to their routes;
app.configure(routes={
    'todos': todo_menu_component,
    'todos.edit': todo_editor_component
})

# Set the starting route;
app.current_route = 'todos'
