from ..console_app_component import ConsoleAppComponent

class TitleBar(ConsoleAppComponent):

    def print(self):
        output = self.app.name+'\n'
        return output