from pyconsoleapp.console_app_component import ConsoleAppComponent
from example import ingredient_edit_scope as scope

_TEMPLATE = '''Enter ingredient name (currently {}):
'''


class IngredientNameEditorComponent(ConsoleAppComponent):

    def run(self):
        self.guard_exit('home.ingredients.new', 'IngredientSaveCheckComponent')

    def print(self):
        output = _TEMPLATE.format(scope.ingredient_name)
        output = self.get_component('StandardPageComponent').print(output)
        return output

    def dynamic_response(self, response):
        self.app.set_window_text(response)
        self.app.show_text_window()
        self.app.info_message = 'Ingredient name set.'
        self.goto('..')
