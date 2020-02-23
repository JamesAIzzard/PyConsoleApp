class ConsoleAppPage():
    def __init__(self):
        self.app = None
        self._components = []
        self._check_static_response_uniqueness()

    def __str__(self):
        output = ''
        for component in self._components:
            output = output+component.printer()
        return output

    def _check_static_response_uniqueness(self):
        signatures = []
        for component in self._components:
            for signature in component.static_response_signatures:
                if signature in signatures:
                    raise KeyError('Duplicated static response.')
                else:
                    signatures.append(signature)

    def _get_static_response_function(self, response):
        for component in self._components:
            if response in component.static_responses:
                return getattr(component, component.get_static_response_func_name(response))

    def _response_is_static(self, response):
        for component in self._components:
            if response in component.static_responses:
                return True
        return False

    def set_component_app_ref(self, app):
        for component in self._components:
            component.app = app

    def add_component(self, component):
        self._components.append(component)

    def process_response(self, response):
        if self._response_is_static(response):
            response_func = self._get_static_response_function(response)
            response_func()      
        else:
            self.dynamic_response(response)

    def dynamic_response(self, response):
        pass
