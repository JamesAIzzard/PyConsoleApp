from pyconsoleapp.console_app import ConsoleApp
from pages.home import home as home_page
from pages.ingredient_menu import ingredient_menu as ingredient_menu_page

app = ConsoleApp('PyDiet')
app.add_route(['home'], home_page)
app.add_route(['home', 'ingredients'], ingredient_menu_page)
app.run()
