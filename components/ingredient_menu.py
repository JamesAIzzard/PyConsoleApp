from pyconsoleapp.console_app_component import ConsoleAppComponent

_MENU_TEMPLATE = '''Choose an option:
(1) - Create a new ingredient.
(2) - Edit an existing ingredient.
(3) - Delete an existing ingredient.
(4) - View an existing ingredient.
'''


class IngredientMenuComponent(ConsoleAppComponent):

    def run(self):
        self.set_ingredient_edit_prompt()
        output = _MENU_TEMPLATE
        output = self.run_parent('standard_page', output)
        return output

    def set_ingredient_edit_prompt(self):
        guard_route = ['home', 'ingredients', 'new']
        
        def yes_edit():
            self.app.clear_entrance(guard_route)
            self.app.navigate(guard_route)
        
        def no_dont_edit():
            self.app.navigate_back()

        self.app.configure_component('yes_no_dialog', {
            'data': {
                'message': 'Do you really want to create a new ingredient?'
            },
            'option_responses': {
                'y': yes_edit,
                'n': no_dont_edit
            }
        })
        self.app.guard_entrance(guard_route, 'yes_no_dialog')

    def on_create(self):
        # self.app.set_window_text('Some test text.')
        # self.app.show_text_window()
        self.app.navigate(['home', 'ingredients', 'new'])

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
    
ingredient_menu = IngredientMenuComponent()
ingredient_menu.set_option_response('1', 'on_create')
ingredient_menu.set_option_response('2', 'on_edit')
ingredient_menu.set_option_response('3', 'on_delete')
ingredient_menu.set_option_response('4', 'on_view')
