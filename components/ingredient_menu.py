from pyconsoleapp.console_app_component import ConsoleAppComponent

_MENU_TEMPLATE = '''Choose an option:
1 -> Create a new ingredient.
2 -> Edit an existing ingredient.
3 -> Delete an existing ingredient.
4 -> View an existing ingredient.
'''


class IngredientMenuComponent(ConsoleAppComponent):

    @property
    def output(self):
        self.parent_component = 'standard_page'
        output = _MENU_TEMPLATE
        return output

    def on_create(self):
        self.app.set_window_text('Some test text.')
        self.app.show_text_window()

    def on_edit(self):
        raise NotImplementedError

    def on_delete(self):
        raise NotImplementedError

    def on_view(self):
        raise NotImplementedError
    
    def dynamic_response(self, response):
        self.app.set_window_text(response)
        self.app.show_text_window()
    
ingredient_menu = IngredientMenuComponent()
ingredient_menu.set_option_response('1', 'on_create')
ingredient_menu.set_option_response('2', 'on_edit')
ingredient_menu.set_option_response('3', 'on_delete')
ingredient_menu.set_option_response('4', 'on_view')
