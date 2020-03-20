from pyconsoleapp.console_app import ConsoleApp

app = ConsoleApp('PyDiet')

app.register_component_package('components')

app.add_root_route(['home'], 'MainMenu')
app.add_route(['home', 'ingredients'], 'IngredientMenu')
app.add_route(['home', 'ingredients', 'new'], 'IngredientEditMenu')
app.add_route(['home', 'ingredients', 'new', 'name'], 'IngredientNameEditor')
app.run()