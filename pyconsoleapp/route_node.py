from typing import Dict, Type, TYPE_CHECKING

from pyconsoleapp import Component, exceptions

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp

class RouteNode:
    def __init__(self, app:'ConsoleApp', route: str, main_component: Type['Component']):
        self._route: str = route
        self._component_state_map: Dict[str: 'Component'] = {
            "main": main_component(app=app)
        }
        self._current_state: str = 'main'

    @property
    def current_state(self) -> str:
        """Return's the node's current state."""
        return self._current_state

    @current_state.setter
    def current_state(self, state: str) -> None:
        """Set's the route node's current state."""
        self._validate_state(state)
        self._current_state = state

    def _validate_state(self, state: str) -> None:
        """Checks the route node has the state specified."""
        if state not in self._component_state_map:
            raise exceptions.StateNotFoundError
