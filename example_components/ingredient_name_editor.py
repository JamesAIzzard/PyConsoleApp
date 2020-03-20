from pyconsoleapp.console_app_component import ConsoleAppComponent

_TEMPLATE = '''Enter ingredient name (currently {}):
'''

class IngredientNameEditor(ConsoleAppComponent):

    def print(self):
        output = _TEMPLATE.format(self.app.data.ingredient_name)
        output = self.app.get_component('StandardPage').print(output)
        return output

    def dynamic_response(self, response):
        # Set a data attribute on the home route, to demonstrate
        # setting route data at a distance;
        self.app.data(['home']).ingredient_created = True
        self.app.set_window_text(response)
        self.app.show_text_window()
        self.app.navigate_back()