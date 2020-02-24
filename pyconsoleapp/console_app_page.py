from pyconsoleapp.console_app import ConsoleApp

class ConsoleAppPage():
    def __init__(self):
        self.app:ConsoleApp = None
        self._components = []
        self._check_option_response_uniqueness()

    def __str__(self):
        output = ''
        for component in self._components:
            output = output+component.get_screen()
        return output

    def _get_option_response_function(self, response):
        for component in self._components:
            if response in component.option_responses:
                return getattr(component, component.get_option_response_func_name(response))

    def _response_is_option(self, response):
        for component in self._components:
            if response in component.option_responses:
                return True
        return False

    def set_component_app_ref(self, app):
        for component in self._components:
            component.app = app

    def use_component(self, component):
        self._components.append(component)

    def process_response(self, response):
        if self._response_is_option(response):
            response_func = self._get_option_response_function(response)
            response_func()      
        else:
            for component in self._components:
                component.dynamic_response(response)
