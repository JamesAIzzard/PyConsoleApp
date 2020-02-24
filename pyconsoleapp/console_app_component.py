from pyconsoleapp.console_app import ConsoleApp

class ConsoleAppComponent():
    def __init__(self):
        self._option_responses = {}
        self._child = None           
        self._siblings = {}
        self.app:ConsoleApp = None

    def __str__(self):
        return self.output

    @property
    def option_responses(self):
        return self._option_responses.keys()

    @property
    def output(self):
        raise NotImplementedError

    def add_component(self, component_name):
        if not component_name in self._siblings.keys():
            self._siblings[component_name] = self.app.components[component_name]
        return self._siblings[component_name].output

    def parent_component(self, parent_name):
        parent = self.app.get_component(parent_name)
        parent.add_child(self)
        return parent.output
    
    def child_output(self):
        return self._child.output

    def set_option_response(self, signature, response_func_name):
        self._option_responses[signature] = response_func_name
        
    def dynamic_response(self, response):
        pass    
