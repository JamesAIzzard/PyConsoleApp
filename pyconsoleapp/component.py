import abc
from typing import List, Dict, Callable, Optional, Type, TypeVar, TYPE_CHECKING

from pyconsoleapp import exceptions
from pyconsoleapp.responder import Responder

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pyconsoleapp.responder_args import ResponderArg

T = TypeVar('T')


class Component(abc.ABC):
    """Base class for all application components."""
    def __init__(self, app: 'ConsoleApp', **kwds):
        self._app = app
        self._current_state: str = 'main'
        self._local_responders_: List['Responder'] = []
        self._get_view_prefill: Optional[Callable[..., str]] = None
        self._local_components_: List['Component'] = []
        self._state_component_map: Dict[str, 'Component'] = {
            "main": self
        }

    @property
    def app(self) -> 'ConsoleApp':
        """Returns the component's app reference."""
        return self._app

    @abc.abstractmethod
    def printer(self, **kwds) -> str:
        """Abstract method responsible for rendering the component view into text."""
        raise NotImplementedError

    def on_load(self) -> None:
        """Method run immediately before the view is extracted from the component."""

    def _validate(self) -> None:
        """Checks the component is valid. Raises an exception if not."""
        # Check there are not multiple local ArglessResponders or markerless args;
        argless_found = False
        markerless_found = False
        for responder in self._local_responders_:
            if responder.is_argless:
                if argless_found is False:
                    argless_found = True
                elif argless_found is True:
                    raise exceptions.DuplicateArglessResponderError
            if responder.has_markerless_arg:
                if markerless_found is False:
                    markerless_found = True
                elif markerless_found is True:
                    raise exceptions.DuplicateMarkerlessArgError

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
        return self._current_state

    @current_state.setter
    def current_state(self, state: str) -> None:
        """Sets the component's current state."""
        self._validate_state(state)
        self._current_state = state

    def get_state_changer(self, new_state: str) -> Callable[[], None]:
        def changer():
            self.current_state = new_state

        return changer

    @property
    def local_components(self) -> List['Component']:
        """Returns the child components for this component."""
        return self._local_components_

    @property
    def active_components(self) -> List['Component']:
        """Returns the components associated with the current state."""
        return self._get_state_components(self.current_state)

    @property
    def active_primary_component(self) -> 'Component':
        """Returns the primary component associated with the current state, self if the state has not
        been delegated."""
        return self._state_component_map[self.current_state]

    def get_state_primary_component(self, state: str) -> 'Component':
        """Returns the primary component associated with the specified state."""
        self._validate_state(state)
        return self._state_component_map[state]

    def _get_state_components(self, state: str) -> List['Component']:
        """Returns the components associated with the specified state."""
        self._validate_state(state)
        components = []
        # Grab the parent component for the state;
        primary_component = self.get_state_primary_component(state)
        # First add any components used by the parent
        components.extend(primary_component.local_components)
        # Now recursively add their active components;
        for parent_local_component in primary_component.local_components:
            components.extend(parent_local_component.active_components)

        return components

    def configure_responder(self, responder_func: Callable[..., None], args: Optional[List['ResponderArg']] = None):
        """Returns the correct responder type, with it's app reference configured."""
        return Responder(app=self.app, func=responder_func, args=args)

    @property
    def _local_responders(self) -> List['Responder']:
        """Returns the list of responders local to this component."""
        return self._local_responders_

    @property
    def _active_responders(self) -> List['Responder']:
        """Returns a list of active responders for the current state combo."""
        responders = []
        for component in self.active_components:
            responders.extend(component._local_responders)
        return responders

    @property
    def active_argless_responder(self) -> Optional['Responder']:
        """Returns the argless responder for this state combo, if exists, otherwise returns None."""
        argless_responder = None
        for responder in self._active_responders:
            if responder.is_argless:
                if argless_responder is None:
                    argless_responder = responder
                elif argless_responder is not None:
                    raise exceptions.DuplicateArglessResponderError
        return argless_responder

    @property
    def active_markerless_arg_responder(self) -> Optional['Responder']:
        """Returns the component's markerless arg responder, if exists, otherwise returns None."""
        markerless_arg_responder = None
        for responder in self._active_responders:
            if responder.has_markerless_arg:
                if markerless_arg_responder is None:
                    markerless_arg_responder = responder
                elif markerless_arg_responder is not None:
                    raise exceptions.DuplicateMarkerlessArgError
        return markerless_arg_responder

    @property
    def active_marker_arg_responders(self) -> List['Responder']:
        """Returns a list of the component's marker responders."""
        mars = []
        for responder in self._active_responders:
            if not responder.has_markerless_arg and not responder.is_argless:
                mars.append(responder)
        return mars

    def get_view_prefill(self) -> Optional[str]:
        """Returns the prefill for the component."""
        if self._get_view_prefill is not None:
            return self._get_view_prefill()
        else:
            return None

    def delegate_state(self, state: str, component_class: Type[T]) -> T:
        """Assigns the specified component state to another component and returns the component instance."""
        component = component_class(app=self.app)
        self._state_component_map[state] = component
        return component

    def use_component(self, component_class: Type[T]) -> T:
        """Includes the child component in this component instance and returns the child instance."""
        component = component_class(app=self.app)
        self._local_components_.append(component)
        list(set(self._local_components_))  # Use set() to prevent duplication.
        return component

    def configure(self, responders: Optional[List['Responder']] = None,
                  get_prefill: Optional[Callable[[], str]] = None,
                  **kwds) -> None:
        """Sets local responders to list provided, if populated."""
        if responders is not None:
            self._local_responders_ = responders
        self._validate()
        # Swallow any remaining **kwds and check this really is the base class.
        assert not hasattr(super(), 'configure')
