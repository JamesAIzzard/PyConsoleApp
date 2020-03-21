from ..console_app_component import ConsoleAppComponent


class SingleHR(ConsoleAppComponent):
    
    def print(self):
        output = '-'*self.app.configs.terminal_width_chars+'\n'
        return output
