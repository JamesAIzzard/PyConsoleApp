import abc
from typing import List, Dict, Callable, Optional, Type, TypeVar, TYPE_CHECKING

from pyconsoleapp import exceptions

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pyconsoleapp.responders import Responder, ArglessResponder

T = TypeVar('T')


class Component(abc.ABC):
    def __init__(self, app: 'ConsoleApp', **kwds):
        self._app_ = app
        self._current_state: Optional[str] = None
        self._state_responder_map: Dict[str, 'Responder'] = {}
        self._state_printer_map: Dict[str, Callable[[], str]] = {}
        self._get_view_prefill: Optional[Callable[[], str]] = None
        self._state_component_map: Dict[str, List['Component']] = {}

        self._validate()

    @property
    def _app(self) -> 'ConsoleApp':
        """Returns the component's app reference."""
        return self._app_

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
        if state not in self._states:
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
    def get_active_components(self) -> List['Component']:
        """Returns the components associated with the current state."""
        return self.get_state_components(self.current_state)

    def get_state_components(self, state: str) -> List['Component']:
        """Returns the component associated with the specified state."""
        self._validate_state(state)
        components = []
        for component in self._state_component_map[state]:
            components.extend(component.)
        return self._state_component_map[state]

    @abc.abstractmethod
    def printer(self, **kwds) -> str:
        """Abstract method responsible for rendering the component view into text."""
        raise NotImplementedError

    def argless_responder(self) -> Optional['ArglessResponder']:
        """Returns the component's argless responder, if exists, otherwise returns None."""
        for responder in self._responders:
            if type(responder, ArglessResponder):
                return responder
        return None

    def current_markerless_responder(self) -> Optional['Responder']:
        """Returns the component's markerless responder, if exists, otherwise returns None."""
        for responder in self._responders:
            if responder.is_markerless:
                return responder
        return None

    def current_marker_responders(self) -> List['Responder']:
        """Returns a list of the component's marker responders."""
        mrs = []
        for responder in self._responders:
            if not responder.is_markerless and not type(responder, ArglessResponder):
                mrs.append(responder)
        return mrs

    def get_view(self) -> str:
        """Returns the view for the component, and adds this component, and its children to the active
        component register."""
        self._app.activate_responders(self._active_responders)
        return self.printer()

    def get_view_prefill(self) -> Optional[str]:
        """Returns the prefill for the component."""
        return self._get_view_prefill()

    def _assign_state_to_component(self, state: str, component_class: Type[T]) -> T:
        """Assigns the specified component state to another component and returns the component instance."""
        component = component_class(app=self._app)
        self._state_component_map[state] = component
        self._child_components_.append(component)
        list(set(self._child_components_))
        return component

    def _use_component(self, component_class: Type[T], state: str = 'main') -> T:
        """Includes the child component in this component instance and returns the child instance."""
        component = component_class(app=self._app)
        self._child_components_.append(component)
        list(set(self._child_components_))
        return component

    def _configure_state(self, state_name: str = 'main', printer: Optional[Callable[[], str]] = None,
                         get_prefill: Optional[Callable[[], str]] = None,
                         responders: Optional[List['Responder']] = None):
        """Configures a component state."""
        raise NotImplementedError

    def configure(self, **kwds) -> None:
        """Configures the component."""
        # Swallow any remaining **kwds and check this really is the base class.
        assert not hasattr(super(), 'configure')
