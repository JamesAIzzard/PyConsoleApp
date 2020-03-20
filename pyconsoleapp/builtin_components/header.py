from pyconsoleapp.console_app_component import ConsoleAppComponent


class Header(ConsoleAppComponent):

    def print(self):
        output = ''
        output = output+self.app.get_component('TitleBar').print()
        output = output+self.app.get_component('DoubleHR').print()
        output = output+self.app.get_component('NavOptions').print()
        output = output+self.app.get_component('NavTrail').print()
        output = output+self.app.get_component('SingleHR').print()
        output = output+self.app.get_component('MessageBar').print()
        return output
