from pyconsoleapp.console_app_component import ConsoleAppComponent

class MessageBar(ConsoleAppComponent):
    
    def run(self):
        output = ''
        if self.app.error_message:
            output = output+'/!\\ Error: {}\n'.format(self.app.error_message)
            output = output+('-'*self.app.terminal_width_chars)+'\n'
            self.app.error_message = None
        if self.app.info_message:
            output = output+'[i] Info: {}\n'.format(self.app.info_message)
            output = output+('-'*self.app.terminal_width_chars)+'\n'
            self.app.info_message = None
        return output

message_bar = MessageBar()