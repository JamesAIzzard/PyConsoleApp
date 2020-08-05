from pyconsoleapp import ConsoleAppComponent, configs

class SingleHrComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app) 
        self.set_print_function(self.print_view)

    def print_view(self):
        output = '-'*configs.terminal_width_chars+'\n'
        return output
