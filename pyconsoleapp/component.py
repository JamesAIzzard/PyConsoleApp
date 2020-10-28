import abc
from typing import List, Callable, Optional, Type, TypeVar, TYPE_CHECKING

from pyconsoleapp import exceptions
from pyconsoleapp.responder import Responder
from pyconsoleapp.route_node import RouteNode

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pyconsoleapp.responder_args import ResponderArg

T = TypeVar('T')


class Component(abc.ABC):
    """Base class for all application components."""

    def __init__(self, app: 'ConsoleApp', route_node: Optional['RouteNode'] = None, **kwds):
        self._app = app
        self._route_node: Optional['RouteNode'] = route_node
        self._local_responders: List['Responder'] = []  # 'local' indicates on *this* instance, not children.
        self._get_view_prefill: Optional[Callable[..., str]] = None
        self._child_components: List['Component'] = []

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
    def route_states(self) -> List[str]:
        """Returns a list of all the route's states."""
        return self._route_node.states

    def _validate_state(self, state: str) -> None:
        """Validates the specified state name."""
        if state not in self.route_states:
            raise exceptions.StateNotFoundError

    @property
    def current_state(self) -> str:
        """Returns the component's current state."""
        return self._route_node.current_state

    @current_state.setter
    def current_state(self, state: str) -> None:
        """Sets the component's current state."""
        self._validate_state(state)
        self._route_node.current_state = state

    def get_state_changer(self, new_state: str) -> Callable[[], None]:
        def changer():
            self.current_state = new_state

        return changer

    # @property
    # def active_components(self) -> List['Component']:
    #     """Returns the components associated with the current state."""
    #     components = [self.get_state_component()]
    #     components.extend(self.get_state_component().active_components)
    #     return components
    #
    # def get_state_component(self, state: Optional[str] = None) -> 'Component':
    #     """Returns the primary component associated with the specified state. If no state is specified,
    #     returns the current state component."""
    #     if state is None:
    #         state = self.current_state
    #     else:
    #         self._validate_state(state)
    #     return self._sibling_components[state]

    def configure_responder(self, responder_func: Callable[..., None], args: Optional[List['ResponderArg']] = None):
        """Returns the correct responder type, with it's app reference configured."""
        return Responder(app=self.app, func=responder_func, args=args)

    @property
    def active_responders(self) -> List['Responder']:
        """Returns a list of active responders for the current state combo."""
        responders = []
        for component in self._route_node.active_components:
            responders.extend(component._local_responders)
        return responders

    @property
    def active_argless_responder(self) -> Optional['Responder']:
        """Returns the argless responder for this state combo, if exists, otherwise returns None."""
        argless_responder = None
        for responder in self.active_responders:
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
        for responder in self.active_responders:
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
        for responder in self.active_responders:
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
        self._sibling_components[state] = component
        return component

    def use_component(self, component_class: Type[T]) -> T:
        """Includes the child component in this component instance and returns the child instance."""
        component = component_class(app=self.app)
        self._child_components.append(component)
        list(set(self._child_components))  # Use set() to prevent duplication.
        return component

    def configure(self, responders: Optional[List['Responder']] = None,
                  get_prefill: Optional[Callable[[], str]] = None,
                  **kwds) -> None:
        """Sets local responders to list provided, if populated."""
        if responders is not None:
            self._local_responders.extend(responders)
        if get_prefill is not None:
            self._get_view_prefill = get_prefill
        self._validate()
        # Swallow any remaining **kwds and check this really is the base class.
        assert not hasattr(super(), 'configure')
