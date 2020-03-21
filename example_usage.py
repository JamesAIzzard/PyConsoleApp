from pyconsoleapp.console_app import ConsoleApp

app = ConsoleApp('PyDiet')

app.register_component_package('example_components')

app.add_root_route(['home'], 'MainMenu')
app.add_route(['home', 'ingredients'], 'IngredientMenu')
app.add_route(['home', 'ingredients', 'new'], 'IngredientEditMenu')
app.add_route(['home', 'ingredients', 'new', 'name'], 'IngredientNameEditor')

# Patch configs over the default like this;
app.configure({
    'terminal_width_chars': 70,
    'some_random_config': 42
})

app.run()