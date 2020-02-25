from pyconsoleapp.console_app_component import ConsoleAppComponent

class DoubleHR(ConsoleAppComponent):
    @property
    def output(self):
        output = '='*self.app.terminal_width_chars+'\n'
        return output

double_hr = DoubleHR()