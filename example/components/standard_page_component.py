from pyconsoleapp.console_app_component import ConsoleAppComponent

class StandardPageComponent(ConsoleAppComponent):

    def print(self, page_content):
        output = ''
        output = output+self.app.get_component('HeaderComponent').print()
        output = output+'{}'.format(page_content)
        return output