from pyconsoleapp.console_app_component import ConsoleAppComponent

class HeaderComponent(ConsoleAppComponent):
    
    def get_screen(self):
        output = '{}:\n'.format(self.app.name)
        output = output+('='*self.app.terminal_width_chars)+'\n'
        trail = ''
        for stage in self.app.route:
            trail = trail+stage.replace('_', ' ')+'>'
        output = output+trail+'\n'        
        output = output+('-'*self.app.terminal_width_chars)+'\n'
        output = output+'(b)ack, (q)uit\n'
        output = output+('='*self.app.terminal_width_chars)+'\n'
        if self.app.error_message:
            output = output+'/!\\ Error: {}\n'.format(self.app.error_message)
            output = output+('-'*self.app.terminal_width_chars)+'\n'
            self.app.error_message = None
        if self.app.info_message:
            output = output+'(i) Info: {}\n'.format(self.app.info_message)
            output = output+('-'*self.app.terminal_width_chars)+'\n'
            self.app.info_message = None
        return output

    def on_back(self):
        self.app.hide_text_window()
        self.app.navigate_back()

    def on_quit(self):
        self.app.clear_console()
        self.app.quit()


header = HeaderComponent()
header.set_static_response('b', 'on_back')
header.set_static_response('q', 'on_quit')
