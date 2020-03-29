from pyconsoleapp.console_app_component import ConsoleAppComponent

_TEMPLATE = '''Choose an option:
(1) - Set ingredient name.
(2) - Set ingredient flags.
(3) - Set a macronutrient.
(4) - Set a micronutrient.
'''

GUARD_ROUTE = ['home', 'ingredients', 'new']


class IngredientEditMenuComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self.set_option_response('1', self.on_set_name)

    def print(self):
        output = _TEMPLATE
        output = self.get_component('standard_page_component').print(output)
        return output

    def on_set_name(self):
        self.goto('.name')

