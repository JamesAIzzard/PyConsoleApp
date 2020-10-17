from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent

from todo_app import service

if TYPE_CHECKING:
    from todo_app.todo import Todo

_template = '''
Update the todo_item and press enter.
'''

class TodoEditorComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.subject:'Todo'
        self.configure_printer(self.print_view)
        self.configure_responder(self.on_enter, args=[
            self.configure_std_primary_arg(name='todo_item', markers=[None]),
            self.configure_valueless_option_arg(name='today', markers=['--today', '-t']),
            self.configure_std_option_arg(name='importance', markers=['--importance', '-i'],
                                          validators=[service.validate_importance_score], default_value=1)
        ])

    def print_view(self):
        output = self.app._get_cached_component('standard_page_component').print(
            page_title='Todo Editor:',
            page_content=_template
        )
        return output, self.subject.text

    def on_enter(self, args):
        # Update the response;
        self.subject.text = args['todo_item']
        self.subject.today = args['today']
        self.subject.importance = args['importance']
        # Head back to the menu;
        self.app.go_to('todos')