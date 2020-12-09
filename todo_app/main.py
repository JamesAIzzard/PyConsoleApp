from pyconsoleapp import ConsoleApp, builtin_components

from todo_app import cli

# Create the app instance;
app = ConsoleApp('Example Todo App')

# Instantiate basic page components;
title_bar_component = builtin_components.TitleBarComponent(title=app.name, tagline='Dietary Optimisiation Software')
message_bar_component = builtin_components.MessageBarComponent()
nav_options_component = builtin_components.NavOptionsComponent(on_back=app.go_back, on_quit=app.quit,
                                                               get_current_route=app.get_current_route)
header_component = builtin_components.HeaderComponent(title_bar_component=title_bar_component,
                                                      nav_options_component=nav_options_component,
                                                      message_bar_component=message_bar_component)
page_component = builtin_components.StandardPageComponent(header_component=header_component)

# Instantiate custom cli components;
todo_dash_component = cli.TodoDashComponent(standard_page_component=page_component)
todo_save_check_component = cli.TodoSaveCheckComponent()
todo_editor_component = cli.TodoEditorComponent(standard_page_component=page_component,
                                                todo_dash_component=todo_dash_component,
                                                save_check_component=todo_save_check_component)
todo_menu_component = cli.TodoMenuComponent(dash_component=todo_dash_component,
                                            editor_component=todo_editor_component,
                                            page_component=page_component)

# Bind the components to their routes;
app.configure(routes={
    'todos': todo_menu_component,
    'todos.edit': todo_editor_component
})

# Set the starting route;
app.current_route = 'todos'
