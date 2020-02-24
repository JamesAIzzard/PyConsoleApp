from pyconsoleapp.console_app_component import ConsoleAppComponent

class HeaderComponent(ConsoleAppComponent):
    
    def output(self):
        output = ''
        output = output+self.add_component('title_bar')
        output = output+self.add_component('double_hr')
        output = output+self.add_component('nav_trail')
        output = output+self.add_component('nav_options')
        output = output+self.add_component('message_bar')
        output = output+self.add_component('single_hr')
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
