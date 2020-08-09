from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent

from example import todo_service

if TYPE_CHECKING:
    from example.todo import Todo

_template = '''
Update the todo and press enter.
'''

class TodoEditorComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.subject:'Todo'
        self.configure_printer(self.print_view)
        self.configure_responder(self.on_enter, args=[
            self.configure_primary_arg(name='todo', markers=[None]),
            self.configure_option_arg(name='today', markers=['--today', '-t']),
            self.configure_option_arg(name='importance', markers=['--importance', '-i'],
                validators=[todo_service.validate_importance_score])
        ])

    def print_view(self):
        output = self.app.fetch_component('standard_page_component').print(
            page_title='Todo Editor:',
            page_content=_template
        )
        return output, self.subject.text

    def on_enter(self, args):
        # Update the response;
        self.subject.text = args['todo']
        self.subject.today = args['today']
        self.subject.importance = args['importance']
        # Head back to the menu;
        self.app.goto('todos')