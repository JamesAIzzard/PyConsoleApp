from pyconsoleapp.console_app_component import ConsoleAppComponent

class HeaderComponent(ConsoleAppComponent):
    
    @property
    def output(self):
        output = ''
        output = output+self.use_component('title_bar')
        output = output+self.use_component('double_hr')
        output = output+self.use_component('nav_options')        
        output = output+self.use_component('nav_trail')
        output = output+self.use_component('single_hr')        
        output = output+self.use_component('message_bar')        
        return output

    def on_back(self):
        self.app.hide_text_window()
        self.app.navigate_back()

    def on_quit(self):
        self.app.clear_console()
        self.app.quit()


header = HeaderComponent()
header.set_option_response('b', 'on_back')
header.set_option_response('q', 'on_quit')
