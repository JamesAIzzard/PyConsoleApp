from pyconsoleapp.console_app import ConsoleApp
from components.ingredient_menu import IngredientMenu
from components.main_menu import MainMenu
from components.standard_page import StandardPage
from components.ingredient_edit_menu import IngredientEditMenu
from components.ingredient_name_editor import IngredientNameEditor
from components.ingredient_save_check import IngredientSaveCheck
from components.ingredient_create_check import IngredientCreateCheck

app = ConsoleApp('PyDiet')

app.register_component(IngredientMenu)
app.register_component(MainMenu)
app.register_component(StandardPage)
app.register_component(IngredientEditMenu)
app.register_component(IngredientNameEditor)
app.register_component(IngredientSaveCheck)
app.register_component(IngredientCreateCheck)

app.add_root_route(['home'], 'MainMenu')
app.add_route(['home', 'ingredients'], 'IngredientMenu')
app.add_route(['home', 'ingredients', 'new'], 'IngredientEditMenu')
app.add_route(['home', 'ingredients', 'new', 'name'], 'IngredientNameEditor')
app.run()