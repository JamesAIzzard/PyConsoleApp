import abc
from typing import List, Dict, Callable, Optional, TYPE_CHECKING

from pyconsoleapp import exceptions

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pyconsoleapp.responders import Responder, ArglessResponder


class Component(abc.ABC):
    def __init__(self, app: 'ConsoleApp', **kwds):
        self._app = app
        self._current_state: Optional[str] = None
        self._state_responder_map: Dict[str, 'Responder'] = {}
        self._state_printer_map: Dict[str, Callable[[], str]] = {}
        self._state_component_map: Dict[str, 'Component'] = {}
        self._child_components: List['Component'] = []

    @property
    def app(self) -> 'ConsoleApp':
        """Returns the component's app reference."""
        return self._app

    def on_load(self) -> None:
        """Method run immediately before the view is extracted from the component."""

    def _validate(self) -> None:
        """Checks the component is valid. Raises an exception if not."""
        raise NotImplementedError

    @property
    def _states(self) -> List[str]:
        """Returns a list of all the component's states."""
        return list(self._state_component_map.keys())

    def _validate_state(self, state: str) -> None:
        """Validates the specified state name."""
        if state not in self.states:
            raise exceptions.StateNotFoundError

    @property
    def current_state(self) -> str:
        """Returns the component's current state."""
        if self._current_state is None:
            raise exceptions.NoCurrentStateError
        return self._current_state

    @current_state.setter
    def current_state(self, state: str) -> None:
        self._validate_state(state)
        self._current_state = state

    @property
    def current_state_component(self) -> 'Component':
        """Returns the component associated with this component's current state."""
        return self._state_component_map[self.current_state]

    def get_state_component(self, state:str) -> 'Component':
        """Returns the component associated with the specified state."""
        self._validate_state(state)
        return self._state_component_map[state]

    def _assign_state_to_component(self, state: str, component: 'Component') -> None:
        """Assigns the specified component state to another component."""
        self._state_component_map[state] = component
        if component not in self._child_components:
            self._child_components.append(component)

    def _configure_state(self, state_name: str, printer: Callable[..., str], responders: List['Responder']):
        """Configures a component state."""
        raise NotImplementedError

    def argless_responder(self) -> Optional['ArglessResponder']:
        """Returns the argless responder, for the current state, if exists, otherwise returns None."""
        raise NotImplementedError

    def markerless_responder(self) -> Optional['MarkerlessResponder']:
        """Returns the markerless responder associated with the current state, if exists. Otherwise
        returns None."""
        raise NotImplementedError

    def marker_responders(self) -> List['MarkerResponder']:
        """Returns a list of the marker responders associated with this component."""
        raise NotImplementedError

    def configure(self, **kwds) -> None:
        """Configures the component."""
        raise NotImplementedError
