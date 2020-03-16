from pyconsoleapp.console_app_component import ConsoleAppComponent

class TitleBar(ConsoleAppComponent):

    def run(self):
        output = self.app.name+'\n'
        return output