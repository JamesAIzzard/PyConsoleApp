from pyconsoleapp.console_app import ConsoleApp
from components.ingredient_menu import ingredient_menu
from components.main_menu import main_menu
from components.standard_page import standard_page
from components.ingredient_edit_menu import ingredient_edit_menu
from components.ingredient_name_editor import ingredient_name_editor
from components.ingredient_save_check import ingredient_save_check

app = ConsoleApp('PyDiet')

app.register_component('ingredient_menu', ingredient_menu)
app.register_component('main_menu', main_menu)
app.register_component('standard_page', standard_page)
app.register_component('ingredient_editor_menu', ingredient_edit_menu)
app.register_component('ingredient_name_editor', ingredient_name_editor)
app.register_component('ingredient_save_check', ingredient_save_check)

app.add_root_route(['home'], 'main_menu')
app.add_route(['home', 'ingredients'], 'ingredient_menu')
app.add_route(['home', 'ingredients', 'new'], 'ingredient_editor_menu')
app.add_route(['home', 'ingredients', 'new', 'name'], 'ingredient_name_editor')
app.run()