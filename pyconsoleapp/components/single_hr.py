from pyconsoleapp.console_app_component import ConsoleAppComponent


class SingleHR(ConsoleAppComponent):
    
    @property
    def output(self):
        output = '-'*self.app.terminal_width_chars+'\n'
        return output


single_hr = SingleHR()
