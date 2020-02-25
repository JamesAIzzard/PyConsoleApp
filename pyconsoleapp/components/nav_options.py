from pyconsoleapp.console_app_component import ConsoleAppComponent

class NavOptions(ConsoleAppComponent):
    
    @property
    def output(self):
        output = '(b)ack | (q)uit\n'
        return output

    def on_back(self):
        self.app.navigate_back()

    def on_quit(self):
        self.app.quit()

nav_options = NavOptions()
nav_options.set_option_response('b', 'on_back')
nav_options.set_option_response('q', 'on_quit')