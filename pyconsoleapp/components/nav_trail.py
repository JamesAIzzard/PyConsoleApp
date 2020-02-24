from pyconsoleapp.console_app_component import ConsoleAppComponent

class NavTrail(ConsoleAppComponent):
    @property
    def output(self):
        trail = ''
        for stage in self.app.route:
            trail = trail+stage.replace('_', ' ')+'>'
        output = output+trail+'\n'        

nav_trail = NavTrail()