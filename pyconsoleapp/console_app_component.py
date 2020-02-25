from pyconsoleapp.console_app import ConsoleApp
from typing import Dict


class ConsoleAppComponent():
    def __init__(self):
        self._option_responses = {}
        self.children: Dict[str, ConsoleAppComponent] = {}
        self.parents: Dict[str, ConsoleAppComponent] = {}
        self.app: ConsoleApp = None
        self.name: str = None

    def __str__(self):
        return self.output

    @property
    def option_responses(self) -> dict:
        collected_responses = {}
        collected_responses.update(self._option_responses)
        for child in self.children.values():
            collected_responses.update(child.option_responses)
        for parent in self.parents.values():
            collected_responses.update(parent.option_responses)
        return collected_responses

    @property
    def dynamic_responses(self) -> list:
        collected_responses = [self.dynamic_response]
        for child in self.children.values():
            collected_responses.append(child.dynamic_response)
        for parent in self.parents.values():
            collected_responses.append(parent.option_responses)            
        return collected_responses

    @property
    def output(self):
        raise NotImplementedError('Output not implemented on {}'
                                  .format(self.__class__))

    def parent_output(self, parent_name: str, child_output: str) -> str:
        parent = self.app.get_component(parent_name)
        if not parent in self.parents.values():
            self.parents[parent_name] = parent
        if not self in parent.children.values():
            parent.children[self.name] = self
        self.app._temp_child_output = child_output
        return parent.output

    def child_output(self):
        return self.app._temp_child_output

    def process_response(self, response):
        option_responses = self.option_responses
        for option in option_responses.keys():
            if option == response:
                option_responses[option]()
        dynamic_responses = self.dynamic_responses
        for dynamic_response in dynamic_responses:
            dynamic_response(response)

    def use_component(self, component_name):
        component = self.app.get_component(component_name)
        if not component_name in self.children.keys():
            self.children[component_name] = component
        return component.output

    def set_option_response(self, signature, response_func_name):
        response_func = getattr(self, response_func_name)
        self._option_responses[signature] = response_func

    def dynamic_response(self, response):
        pass
