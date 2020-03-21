from pyconsoleapp.console_app_component import ConsoleAppComponent

_TEMPLATE = '''Enter ingredient name (currently {}):
'''


class IngredientNameEditor(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self.scope = self.get_scope('new_ingredient')

    def print(self):
        output = _TEMPLATE.format(self.scope.ingredient_name)
        output = self.app.get_component('StandardPage').print(output)
        return output

    def dynamic_response(self, response):
        self.app.set_window_text(response)
        self.app.show_text_window()
        self.app.navigate_back()
