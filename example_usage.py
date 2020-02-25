from pyconsoleapp.console_app import ConsoleApp
from components.ingredient_menu import ingredient_menu
from components.main_menu import main_menu
from components.standard_page import standard_page

app = ConsoleApp('PyDiet')

app.register_component('ingredient_menu', ingredient_menu)
app.register_component('main_menu', main_menu)
app.register_component('standard_page', standard_page)

app.add_route(['home'], 'main_menu')
app.add_route(['home', 'ingredients'], 'ingredient_menu')
# app.add_route(['home', 'ingredients', 'edit'], 'ingredient_editor')
# app.add_route(['home', 'ingredients', 'edit', 'save?'], 'y_n_query')
app.run()