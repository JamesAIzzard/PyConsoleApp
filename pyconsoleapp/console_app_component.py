from pyconsoleapp.console_app import ConsoleApp
from typing import Dict


class ConsoleAppComponent():
    def __init__(self):
        self.option_responses = {}
        self.app: ConsoleApp = None
        self.name: str = None

    def run(self):
        raise NotImplementedError('Output not implemented on {}'
                                  .format(self.__class__))

    def run_parent(self, parent_name: str, child_output: str) -> str:
        parent = self.app.get_component(parent_name)
        self.app.active_components[parent_name] = parent
        self.app._temp_child_output = child_output
        return parent.output

    def child_output(self):
        return self.app._temp_child_output

    def insert_component(self, component_name):
        component = self.app.get_component(component_name)
        if not component_name in self.children.keys():
            self.children[component_name] = component
        return component.output

    def call_for_option_response(self, signature):
        if signature in self.option_responses.keys():
            self.option_responses[signature]()

    def set_option_response(self, signature, response_func_name):
        response_func = getattr(self, response_func_name)
        self.option_responses[signature] = response_func

    def dynamic_response(self, response):
        pass
