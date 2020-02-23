from pyconsoleapp.console_app_component import ConsoleAppComponent

_MENU_TEMPLATE = '''Choose an option:
1 -> Create a new ingredient.
2 -> Edit an existing ingredient.
3 -> Delete an existing ingredient.
4 -> View an existing ingredient.
'''


class IngredientMenuComponent(ConsoleAppComponent):

    def get_screen(self):
        return _MENU_TEMPLATE

    def on_create(self):
        raise NotImplementedError

    def on_edit(self):
        raise NotImplementedError

    def on_delete(self):
        raise NotImplementedError

    def on_view(self):
        raise NotImplementedError
    
ingredient_menu = IngredientMenuComponent()
ingredient_menu.set_static_response('1', 'on_create')
ingredient_menu.set_static_response('2', 'on_edit')
ingredient_menu.set_static_response('3', 'on_delete')
ingredient_menu.set_static_response('4', 'on_view')