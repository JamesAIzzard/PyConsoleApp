from pyconsoleapp.console_app_component import ConsoleAppComponent

class DoubleHR(ConsoleAppComponent):
    def run(self):
        output = '='*self.app.terminal_width_chars+'\n'
        return output

double_hr = DoubleHR()