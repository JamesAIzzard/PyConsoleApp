from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

class IngredientCreateCheckComponent(YesNoDialogComponent):

    def __init__(self):
        super().__init__()
        self.message = 'Do you really want to create a new ingredient?'
        self.set_option_response('y', self.on_yes_create)
        self.set_option_response('n', self.on_no_dont_create)

    def on_yes_create(self):
        self.clear_entrance('.')

    def on_no_dont_create(self):
        # Navigate back;
        self.goto('..')