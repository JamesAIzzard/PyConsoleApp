from ..console_app_component import ConsoleAppComponent

class NavOptions(ConsoleAppComponent):
    
    def __init__(self):
        super().__init__()
        self.set_option_response('b', self.on_back)
        self.set_option_response('q', self.on_quit)

    def print(self):
        output = '(b)ack | (q)uit\n'
        return output

    def on_back(self)->None:
        self.app.navigate_back()

    def on_quit(self)->None:
        self.app.quit()