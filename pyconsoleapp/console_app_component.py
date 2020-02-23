class ConsoleAppComponent():
    def __init__(self):
        self.app = None
        self._static_responses = {}

    @property
    def static_responses(self):
        return self._static_responses.keys()

    def get_static_response_func_name(self, static_response):
        return self._static_responses[static_response]

    def get_screen(self):
        raise NotImplementedError

    def set_static_response(self, signature, response_func_name):
        self._static_responses[signature] = response_func_name
