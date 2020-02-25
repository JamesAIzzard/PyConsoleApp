from pyconsoleapp.console_app_component import ConsoleAppComponent

class TitleBar(ConsoleAppComponent):

    @property
    def output(self):
        output = self.app.name+'\n'
        return output

title_bar = TitleBar()