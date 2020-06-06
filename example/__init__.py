from pyconsoleapp import ConsoleApp

# Create the main app instance
app = ConsoleApp('Todo App')

# Register the package(s) containing the components;
app.register_component_package('example.components')
# app.register_component_package('example.more_components') # More packages included like this.

# Configure some example routes;
app.root_route('todos', 'TodoMenuComponent') # This is the root app screen.
app.add_route('todos.edit', 'TodoEditorComponent')

# Run the app;
app.run()