from pyconsoleapp.console_app import ConsoleApp

app = ConsoleApp('PyDiet')
app.add_route(['home'], 'home')
app.add_route(['home', 'ingredients'], 'ingredient_menu')
app.add_route(['home', 'ingredients', 'edit'], 'ingredient_editor')
app.add_route(['home', 'ingredients', 'edit', 'save?'], 'y_n_query')
app.run()