from pyconsoleapp.console_app import ConsoleApp
from typing import Callable, Optional, Any

class ConsoleAppComponent():
    def __init__(self):
        self.option_responses = {}
        self.app: ConsoleApp

    @property
    def name(self)->str:
        return self.__class__.__name__

    def run(self) -> Optional[str]:
        raise NotImplementedError('Run not implemented on {}'
                                  .format(self.__class__))

    def run_parent(self, parent_name: str, child_output: str) -> Optional[str]:
        self.app._temp_child_output = child_output
        return self.app.run_component(parent_name)

    def child_output(self):
        return self.app._temp_child_output

    def insert_component(self, component_name:str)->Optional[str]:
        return self.app.run_component(component_name)

    def process_response(self, response:str)->None:
        # First run the dynamic response;
        self.dynamic_response(response)
        # Then run option response if match;
        if response in self.option_responses.keys():
            self.option_responses[response]()

    def set_option_response(self, signature:str, func:Callable)->None:
        self.option_responses[signature] = func

    def dynamic_response(self, response:str)->None:
        pass
