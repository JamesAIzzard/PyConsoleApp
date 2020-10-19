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
        self._local_responder_cache: List['Responder'] = []
        self._get_view_prefill: Optional[Callable[..., str]] = None
        self._local_components: List['Component'] = []
        self._state_component_map: Dict[str, 'Component'] = {
            "main": self
        }

    @property
    def _app(self) -> 'ConsoleApp':
        """Returns the component's app reference."""
        return self._app_

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
        for responder in self._local_responders:
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
    def _local_responders(self) -> List['Responder']:
        """Returns the list of responders belonging to the local components."""
        if len(self._local_responder_cache) is 0:
            for component in self.local_components:
                self._local_responder_cache.extend(component.local_responders)
        return self._local_responder_cache

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
        """Sets the component's current state."""
        self._validate_state(state)
        self._current_state = state

    @property
    def local_components(self) -> List['Component']:
        """Returns the child components for this component."""
        return self._local_components

    @property
    def active_components(self) -> List['Component']:
        """Returns the components associated with the current state."""
        return self.get_state_components(self.current_state)

    def get_state_components(self, state: str) -> List['Component']:
        """Returns the component associated with the specified state."""
        self._validate_state(state)
        # Grab the parent component for the state;
        parent_component = self._state_component_map[state]
        # Add the grandchild components first;
        components = []
        for child_component in self.local_components:
            components.extend(child_component.active_components)
        # Add in the child components;
        components.extend(self.local_components)
        # Add the parent into the final list;
        components.append(parent_component)

        return components

    @property
    def local_responders(self) -> List['Responder']:
        """Returns the list of responders local to this component."""
        return self._local_responders

    @property
    def _active_responders(self) -> List['Responder']:
        """Returns a list of active responders for the current state combo."""
        responders = []
        for component in self.active_components:
            responders.extend(component.local_responders)
        return responders

    def active_argless_responder(self) -> Optional['ArglessResponder']:
        """Returns the argless responder for this state combo, if exists, otherwise returns None."""
        argless_responder = None
        for responder in self._active_responders:
            if type(responder, ArglessResponder):
                if argless_responder is None:
                    argless_responder = responder
                elif argless_responder is not None:
                    raise exceptions.DuplicateArglessResponderError
        return argless_responder

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

    def active_marker_arg_responders(self) -> List['Responder']:
        """Returns a list of the component's marker responders."""
        mars = []
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
