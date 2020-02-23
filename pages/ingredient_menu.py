from pyconsoleapp.console_app_page import ConsoleAppPage
from components.header import header
from components.ingredient_menu import ingredient_menu as ingredient_menu_component

class IngredientMenu(ConsoleAppPage):
    pass

ingredient_menu = IngredientMenu()
ingredient_menu.add_component(header)
ingredient_menu.add_component(ingredient_menu_component)