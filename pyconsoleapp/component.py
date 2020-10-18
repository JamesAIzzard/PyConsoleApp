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
        self._state_component_map: Dict[str, 'Component'] = {}
        self._child_components_: List['Component'] = []

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
    def current_state_component(self) -> 'Component':
        """Returns the component associated with this component's current state."""
        return self.get_state_component(self.current_state)

    @property
    def _child_components(self) -> List['Component']:
        """Returns a list of all child components, including childeren of childeren, etc."""
        child_components = []
        for child in self._child_components_:
            child_components.extend(*child._child_components_)
        return child_components

    def get_state_component(self, state: str) -> 'Component':
        """Returns the component associated with the specified state."""
        self._validate_state(state)
        return self._state_component_map[state]

    @property
    def _current_printer(self) -> Callable[..., str]:
        return self._state_printer_map[self.current_state]

    def current_argless_responder(self) -> Optional['ArglessResponder']:
        """Returns the argless responder, for the current state, if exists, otherwise returns None."""
        raise NotImplementedError

    def current_markerless_responder(self) -> Optional['Responder']:
        """Returns the markerless responder associated with the current state, if exists. Otherwise
        returns None."""
        raise NotImplementedError

    def current_marker_responders(self) -> List['Responder']:
        """Returns a list of the marker responders associated with this component."""
        raise NotImplementedError

    def get_view(self) -> str:
        """Returns the view for the component, and adds this component, and its children to the active
        component register."""
        self._app.activate_components([self, *self._child_components])
        return self._current_printer()

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

    def _use_component(self, component_class: Type[T]) -> T:
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
