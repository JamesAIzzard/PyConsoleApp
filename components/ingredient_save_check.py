from pyconsoleapp.components.YesNoDialog import YesNoDialog

GUARD_ROUTE = ['home', 'ingredients', 'new']
EXIT_TO_ROUTE = ['home', 'ingredients']

class IngredientSaveCheck(YesNoDialog):

    def __init__(self):
        super().__init__()
        self.set_option_response('y', self.on_yes_save)
        self.set_option_response('n', self.on_no_dont_save)
        self.message = 'Save changes to this ingredient?'

    def on_yes_save(self):
        self.app.info_message = 'Ingredient saved.'
        self.app.clear_exit(GUARD_ROUTE)
        self.app.navigate(EXIT_TO_ROUTE)        

    def on_no_dont_save(self):
        self.app.info_message = 'Ingredient not saved.'
        self.app.clear_exit(GUARD_ROUTE)
        self.app.navigate(EXIT_TO_ROUTE)        