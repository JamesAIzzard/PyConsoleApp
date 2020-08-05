from pyconsoleapp.components import ConsoleAppComponent

_template = '''-back, -b -> Navigate back.
-quit, -q -> Quit.
'''

class NavOptionsComponent(ConsoleAppComponent):
    
    def __init__(self, app):
        super().__init__(app)
        self.configure_printer(self.print_view)
        self.configure_responder(self.on_back, args=[
            self.configure_primary_arg(markers=['-back', '-b'])
        ])
        self.configure_responder(self.on_quit, args=[
            self.configure_primary_arg(markers=['-quit', '-q'])
        ])

    def print_view(self):
        return _template

    def on_back(self)->None:
        self.app.goto('..')

    def on_quit(self)->None:
        self.app.quit()