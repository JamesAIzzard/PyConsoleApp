from pyconsoleapp.console_app_component import ConsoleAppComponent

class NavTrail(ConsoleAppComponent):

    def run(self):
        trail = ''
        for stage in self.app.route:
            trail = trail+stage.replace('_', ' ')+'>'
        return trail+'\n'        