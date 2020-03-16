from pyconsoleapp.console_app_component import ConsoleAppComponent


class SingleHR(ConsoleAppComponent):
    
    def run(self):
        output = '-'*self.app.terminal_width_chars+'\n'
        return output
