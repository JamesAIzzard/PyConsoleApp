from pyconsoleapp.components.YesNoDialog import YesNoDialog

class IngredientCreateCheck(YesNoDialog):

    def __init__(self):
        super().__init__()
        self.message = 'Do you really want to create a new ingredient?'
        self.set_option_response('y', self.on_yes_create)
        self.set_option_response('n', self.on_no_dont_create)

    def on_yes_create(self):
        self.app.navigate(['.', 'new'])
        self.app.clear_entrance(['home', 'ingredients', 'new'])

    def on_no_dont_create(self):
        self.app.navigate_back()