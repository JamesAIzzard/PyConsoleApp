from pyconsoleapp.console_app_component import ConsoleAppComponent

_TEMPLATE = '''Choose an option:
(1) - Set ingredient name.
(2) - Set ingredient flags.
(3) - Set a macronutrient.
(4) - Set a micronutrient.
'''


class IngredientEditMenu(ConsoleAppComponent):

    def run(self):
        output = _TEMPLATE
        output = self.run_parent('standard_page', output)
        return output

    def on_set_name(self):
        self.set_save_changes_prompt()
        self.app.navigate(['.', 'name'])

    def set_save_changes_prompt(self):
        guard_route = ['home', 'ingredients', 'new']
        exit_to_route = ['home', 'ingredients']

        def yes_save():
            self.app.info_message = 'Ingredient saved.'
            self.app.clear_exit(guard_route)
            self.app.navigate(exit_to_route)

        def no_dont_save():
            self.app.info_message = 'Ingredient not saved.'
            self.app.clear_exit(guard_route)
            self.app.navigate(exit_to_route)

        self.app.configure_component('yes_no_prompt', {
            'data': {
                'message': 'Do you want to save the ingredient?'
            },
            'option_responses': {
                'y': yes_save,
                'n': no_dont_save
            }
        })
        self.app.guard_exit(['home', 'ingredients', 'new'], 'yes_no_prompt')


ingredient_edit_menu = IngredientEditMenu()
ingredient_edit_menu.set_option_response('1', 'on_set_name')
