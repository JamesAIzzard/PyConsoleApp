from pyconsoleapp.console_app_component import ConsoleAppComponent


class DoubleHR(ConsoleAppComponent):
    def print(self):
        output = '='*self.app.terminal_width_chars+'\n'
        return output
