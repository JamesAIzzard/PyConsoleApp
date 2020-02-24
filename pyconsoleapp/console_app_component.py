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
        # Return option responses for this component
        # and all child components.
        pass

    @property
    def dynamic_responses(self):
        # Return dynamic responses for this component
        # and all child components.
        pass

    @property
    def output(self):
        raise NotImplementedError

    def process_response(self, response):
        option_responses = self.option_responses
        for option in option_responses.keys():
            if option == response:
                option_responses[option]()
        dynamic_responses = self.dynamic_responses
        for dynamic_response in dynamic_responses:
            dynamic_response(response)

    def add_child(self, child):
        self._child = child

    def use_component(self, component_name):
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
        response_func = getattr(self, response_func_name)
        self._option_responses[signature] = response_func
        
    def dynamic_response(self, response):
        pass    
