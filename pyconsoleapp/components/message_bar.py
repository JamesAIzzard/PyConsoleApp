from pyconsoleapp.console_app_component import ConsoleAppComponent

class MessageBar(ConsoleAppComponent):
    @property
    def output(self):
        output = '='*self.app.terminal_width_chars+'\n'
        return output

message_bar = MessageBar()