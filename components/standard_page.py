from pyconsoleapp.console_app_component import ConsoleAppComponent

class StandardPage(ConsoleAppComponent):

    @property
    def output(self):
        output = ''
        output = output+self.add_component('header')
        output = output+self.child_output()
        output = output+self.add_component('double_hr')
        return output