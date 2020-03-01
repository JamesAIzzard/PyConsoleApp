from pyconsoleapp.console_app import ConsoleApp
from typing import Optional, Dict, Any


class ConsoleAppComponent():
    def __init__(self):
        self.option_responses = {}
        self.app: ConsoleApp
        self.name: str
        self.responded_already: bool = False
        self.data: Dict[str, Any] = {} # For storing data in;
        self.state: Dict[str, Any] = {} # For storing state in;

    def run(self) -> Optional[str]:
        raise NotImplementedError('Run not implemented on {}'
                                  .format(self.__class__))

    def run_parent(self, parent_name: str, child_output: str) -> Optional[str]:
        self.app._temp_child_output = child_output
        return self.app.run_component(parent_name)

    def child_output(self):
        return self.app._temp_child_output

    def configure(self, configs: dict) -> None:
        for config_key in configs.keys():
            setattr(self, config_key, configs[config_key])

    def insert_component(self, component_name):
        return self.app.run_component(component_name)

    def process_response(self, response:str)->None:
        if not self.responded_already:
            # First run the dynamic response;
            self.dynamic_response(response)
            # Then run option response if match;
            if response in self.option_responses.keys():
                self.option_responses[response]()
        # Set responded flag;
        self.responded_already = True

    def set_option_response(self, signature, response_func_name):
        response_func = getattr(self, response_func_name)
        self.option_responses[signature] = response_func

    def dynamic_response(self, response):
        pass
