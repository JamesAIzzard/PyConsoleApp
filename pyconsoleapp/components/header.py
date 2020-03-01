from pyconsoleapp.console_app_component import ConsoleAppComponent

class HeaderComponent(ConsoleAppComponent):
    
    def run(self):
        output = ''
        output = output+self.insert_component('title_bar')
        output = output+self.insert_component('double_hr')
        output = output+self.insert_component('nav_options')        
        output = output+self.insert_component('nav_trail')
        output = output+self.insert_component('single_hr')        
        output = output+self.insert_component('message_bar')        
        return output

    def on_back(self):
        self.app.hide_text_window()
        self.app.navigate_back()

    def on_quit(self):
        self.app.clear_console()
        self.app.quit()


header = HeaderComponent()
