from pyconsoleapp.console_app_component import ConsoleAppComponent

class StandardPageComponent(ConsoleAppComponent):

    def print(self, page_content):
        output = ''
        output = output+self.get_component('HeaderComponent').print()
        output = output+'{}'.format(page_content)
        return output