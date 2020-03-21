from abc import abstractmethod, ABC
from .console_app import ConsoleApp
from pinjector import inject
from typing import Callable, Dict, Any


class ConsoleAppComponent(ABC):
    def __init__(self):
        self.option_responses: Dict[str, Callable] = {}
        self.app:'ConsoleApp' = inject('app')

    def __getattribute__(self, name: str) -> Any:
        '''Intercepts the print command and adds the component to
        the app's list of active components.
        
        Arguments:
            name {str} -- Name of the attribute being accessed.
        
        Returns:
            Any -- The attribute which was requested.
        '''
        # If the print method was called;
        if name == 'print':
            # Add this component to the active components list;
            self.app.make_component_active(self.name)
        # Return whatever was requested;
        return super().__getattribute__(name)

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def print(self, *args, **kwargs) -> str:
        pass
    
    def create_scope(self, scope_name:str):
        return self.app._data.create_scope(scope_name)

    def clear_scope(self, scope_name:str):
        self.app._data.clear_scope(scope_name)

    def get_scope(self, scope_name:str):
        return self.app._data.get_scope(scope_name)

    def set_option_response(self, signature: str, func: Callable) -> None:
        self.option_responses[signature] = func

    def dynamic_response(self, response: str) -> None:
        pass
