from pyconsoleapp.console_app_component import ConsoleAppComponent

_MENU_TEMPLATE = '''Choose an option:
(1) - Create a new ingredient.
(2) - Edit an existing ingredient.
(3) - Delete an existing ingredient.
(4) - View an existing ingredient.
'''


class IngredientMenu(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self.set_option_response('1', self.on_create)
        self.set_option_response('2', self.on_edit)
        self.set_option_response('3', self.on_delete)
        self.set_option_response('4', self.on_view)

    def run(self):
        self.app.guard_entrance(['.', 'new'], 'IngredientCreateCheck')
        output = _MENU_TEMPLATE
        output = self.run_parent('StandardPage', output)
        return output

    def on_create(self):
        # self.app.set_window_text('Some test text.')
        # self.app.show_text_window()
        self.app.navigate(['.', 'new'])

    def on_edit(self):
        raise NotImplementedError

    def on_delete(self):
        raise NotImplementedError

    def on_view(self):
        raise NotImplementedError
    
    def dynamic_response(self, response):
        pass
        # self.app.set_window_text(response)
        # self.app.show_text_window()
