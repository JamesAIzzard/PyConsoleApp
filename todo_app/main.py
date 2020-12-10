from pyconsoleapp import ConsoleApp, builtin_components

from todo_app import cli

# Create the app instance;
app = ConsoleApp('Example Todo App')

# Instantiate shared components;
title_bar_component = builtin_components.TitleBarComponent(title=app.name, tagline='Dietary Optimisiation Software')
message_bar_component = builtin_components.MessageBarComponent(),
nav_options_component = builtin_components.NavOptionsComponent(
    on_back=app.go_back,
    on_quit=app.quit,
    get_current_route=app.get_current_route
)
header_component = builtin_components.HeaderComponent(
    title_bar_component=title_bar_component,
    message_bar_component=message_bar_component,
    nav_options_component=nav_options_component
)
todo_editor_component = cli.TodoEditorComponent(nav_on_return=app.get_route_changer('todos'))

# Configure the app routes;
app.configure(routes={
    'todos': cli.TodoMenuComponent(
        todo_editor_component=todo_editor_component,
        editor_route='todos.edit'
    ),
    'todos.edit': todo_editor_component
})

# Set the starting route;
app.current_route = 'todos'
