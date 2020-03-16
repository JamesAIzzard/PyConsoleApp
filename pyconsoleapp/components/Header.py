from pyconsoleapp.console_app_component import ConsoleAppComponent

class Header(ConsoleAppComponent):
    
    def run(self):
        output = ''
        output = output+self.insert_component('TitleBar')
        output = output+self.insert_component('DoubleHR')
        output = output+self.insert_component('NavOptions')        
        output = output+self.insert_component('NavTrail')
        output = output+self.insert_component('SingleHR')        
        output = output+self.insert_component('MessageBar')        
        return output

    def on_back(self):
        self.app.hide_text_window()
        self.app.navigate_back()

    def on_quit(self):
        self.app.clear_console()
        self.app.quit()
