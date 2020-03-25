from pyconsoleapp.console_app_component import ConsoleAppComponent


class HeaderComponent(ConsoleAppComponent):

    def print(self):
        output = ''
        output = output+self.app.get_component('TitleBarComponent').print()
        output = output+self.app.get_component('DoubleHRComponent').print()
        output = output+self.app.get_component('NavOptionsComponent').print()
        output = output+self.app.get_component('NavTrailComponent').print()
        output = output+self.app.get_component('SingleHRComponent').print()
        output = output+self.app.get_component('MessageBarComponent').print()
        return output
