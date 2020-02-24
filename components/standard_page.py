from pyconsoleapp.console_app_component import ConsoleAppComponent

class StandardPage(ConsoleAppComponent):

    @property
    def output(self):
        output = ''
        output = output+self.add_component('title_bar')
        output = output+self.add_component('double_hr')
        output = output+self.add_component('nav_trail')
        output = output+self.add_component('single_hr')
        output = output+self.add_component('nav_options')
        output = output+self.child_output()
        output = output+self.add_component('double_hr')
        return output