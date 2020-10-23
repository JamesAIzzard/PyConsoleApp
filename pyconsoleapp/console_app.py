import os
from typing import Dict, List, Optional, TYPE_CHECKING, Type, TypeVar

if os.name == 'nt':
    from pyautogui import write
else:
    import readline

from pyconsoleapp import exceptions, configs

if os.name == 'nt':
    from pyautogui import write
else:
    import readline

if TYPE_CHECKING:
    from pyconsoleapp import Component, GuardComponent, PopupComponent

T = TypeVar('T')


def _write_to_screen(view: str, prefill: Optional[str]):
    """Adds the option of prefill to the normal input() function."""
    if prefill is None:
        prefill = ''
    if os.name == 'nt':
        write(prefill)
        return input(view)
    else:
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(view)
        finally:
            readline.set_startup_hook()


class ConsoleApp:
    def __init__(self, name):
        self._response: Optional[str] = None
        self._root_route: Optional[str] = None
        self._current_route: Optional[str] = None
        self._route_history: List[str] = []
        self._route_component_map: Dict[str, 'Component'] = {}
        self._route_exit_guard_map: Dict[str, 'GuardComponent'] = {}
        self._route_entrance_guard_map: Dict[str, 'GuardComponent'] = {}
        self._active_popups_: List['PopupComponent'] = []
        self._finished_processing_response: bool = False
        self._quit: bool = False
        self._name: str = name
        self.error_message: Optional[str] = None
        self.info_message: Optional[str] = None

    @property
    def name(self) -> str:
        """Gets application name."""
        return self._name

    @property
    def current_route(self) -> str:
        """Gets the current application route."""
        if self._current_route == '':
            return self._root_route
        else:
            return self._current_route

    @current_route.setter
    def current_route(self, route: str) -> None:
        """Sets the current application route."""
        if route in self._route_component_map.keys():
            self._current_route = route
        else:
            raise KeyError('The route {} was not recognised.'.format(route))

    @property
    def root_route(self) -> str:
        """Gets the application's root route."""
        if self._root_route is None:
            raise exceptions.NoRootRouteError
        return self._root_route

    def add_root_route(self, route: str, component_class: Type['Component']) -> None:
        """Sets the application's route root and assigns its component."""
        if self._root_route is not None:
            raise exceptions.RootRouteAlreadyConfiguredError
        self._root_route = route
        self.add_route(route, component_class)

    def add_route(self, route: str, component_class: Type['Component']) -> None:
        """Configures a new application root and assigns its component."""
        if route in self._route_component_map:
            raise exceptions.RouteAlreadyExistsError
        self._route_component_map[route] = component_class(app=self)

    def _validate_route(self, route: str):
        if route not in self._route_component_map:
            raise exceptions.InvalidRouteError

    def _historise_route(self, route: str) -> None:
        # Save the current route to the history;
        self._route_history.append(route)
        # Make sure the history doesn't get too long;
        while len(self._route_history) > configs.route_history_length:
            self._route_history.pop(0)

    def get_component(self, route: str, state: str) -> 'Component':
        """Gets the component associated with the specified route and state."""
        self._validate_route(route)
        component = self._route_component_map[route]
        return component.get_state_primary_component(state)

    @property
    def _current_primary_component(self) -> 'Component':
        """Returns the primary component associated with the current app route, or a popup if one is active."""
        popup = self._active_popup
        if popup is not None:
            return popup
        else:
            return self._route_component_map[self.current_route].active_primary_component

    def activate_popup(self, popup: 'PopupComponent') -> None:
        """Adds the specified popup to the list of active popups."""
        self._active_popups_.append(popup)

    def deactivate_popup(self, popup: 'PopupComponent') -> None:
        """Removes the specified popup from the list of active popups, if present."""
        self._active_popups_.remove(popup)

    @property
    def _active_popup(self) -> Optional['PopupComponent']:
        """Returns the next active popup component, or None if no popup is active."""
        if len(self._active_popups_) > 0:
            return self._active_popups_[0]
        active_guard = self._get_active_guard()
        if active_guard is not None:
            return active_guard
        else:
            return None

    def _get_active_guard(self) -> Optional['GuardComponent']:
        """Returns the active guard if exists, otherwise returns None."""
        # First check the exit guards;
        for guarded_route in self._route_exit_guard_map.keys():
            # If the guarded root does not feature in the submitted route;
            if guarded_route not in self.current_route:
                # The submitted route must have exited, so populate the component;
                return self._route_exit_guard_map[guarded_route]
        # Now check the entrance guards;
        for guarded_route in self._route_entrance_guard_map.keys():
            # If the guarded root is part of the submitted route;
            if guarded_route in self.current_route:
                # Then the submitted route must be beyond the guard, so populate the
                # component;
                return self._route_entrance_guard_map[guarded_route]
        # No active guards;
        return None

    def guard_entrance(self, route_to_stay_outside: str, guard: 'GuardComponent'):
        """Assigns the guard to the entrance of the specified route."""
        self._validate_route(route_to_stay_outside)
        self._route_entrance_guard_map[route_to_stay_outside] = guard

    def guard_exit(self, route_to_stay_within: str, guard: 'GuardComponent'):
        """Assigns the guard to the exit of the specified route."""
        self._validate_route(route_to_stay_within)
        self._route_exit_guard_map[route_to_stay_within] = guard

    def clear_entrance(self, route: str) -> None:
        """Clears any guard from the entrance of the specified route."""
        self._validate_route(route)
        if route in self._route_entrance_guard_map.keys():
            del self._route_entrance_guard_map[route]

    def clear_exit(self, route: str) -> None:
        """Clears any guard from the exit of the specified route."""
        self._validate_route(route)
        if route in self._route_exit_guard_map.keys():
            del self._route_exit_guard_map[route]

    def _process_response(self, response: str) -> None:
        """Processes the response provided.
        - If the response is empty, the active cli are searched for an empty responder, which, if found, is
        called with no arguments.
        - If the response is not empty the active cli are searched for a matching marker-responder, which
        if found, is called with the response as an argument.
        - If no marker responders are found, the active cli are searched for a markerless responder, which if
        found, is called with the response as an argument."""
        responder_was_found = False
        try:
            # If the response is empty, give each active component a chance to respond;
            if response.replace(' ', '') == '':
                for component in self._active_components:
                    argless_responder = component.active_argless_responder
                    if argless_responder:
                        argless_responder.respond()
                        responder_was_found = True
                        if self._finished_processing_response:
                            return

            # Otherwise, give any marker-only responders a chance;
            else:
                for component in self._active_components:
                    responders = component.active_marker_arg_responders
                    if len(responders):
                        for responder in responders:
                            if responder.check_response_match(response):
                                responder.respond(response)
                                responder_was_found = True
                                if self._finished_processing_response:
                                    return

            # Finally give each active component a chance to field a
            # markerless responder;
            for component in self._active_components:
                markerless_responder = component.active_markerless_arg_responder
                if markerless_responder:
                    markerless_responder.respond(response)
                    responder_was_found = True
                    if self._finished_processing_response:
                        return

            # If no component has responded, then raise an exception;
            if not responder_was_found and not response.replace(' ', '') == '':
                raise exceptions.ResponseValidationError('This response isn\'t recognised.')

        except exceptions.ResponseValidationError as e:
            if e.reason is not None:
                self.error_message = e.reason
            return

    def _clear_response(self):
        """Resets the response fields, ready for the next response collection cycle."""
        self._response = None
        self._finished_processing_response = False

    # TODO - We need to think about how these next two control the response search from within Component.
    # - Ideally we need this to default to halting the response cycle when a response occurs. Like an opt-back-in
    # scheme.
    def continue_responding(self) -> None:
        """Instructs the application to continue searching for responders."""
        self._finished_processing_response = False

    def stop_responding(self) -> None:
        """Instructs the application to stop searching for responders."""
        self._finished_processing_response = True

    def run(self) -> None:
        """Main run loop for the CLI."""
        while not self._quit:
            # If response has been collected;
            if self._response is not None:
                # Do the processing;
                self._process_response(self._response)
                self._clear_response()

            # The response has not been collected, draw the view and collect it;
            else:
                component = self._current_primary_component
                component.on_load()

                # Check the component is still the right one after the load method ran.
                if not component == self._current_primary_component:
                    continue

                self.clear_console()
                # Only add the component to the history if it wasn't a popup.
                if component is not type(PopupComponent):
                    self._historise_route(self.current_route)

                self._response = _write_to_screen(view=component.printer(), prefill=component.get_view_prefill())

    def go_to(self, route: str) -> None:
        """Navigates the application the specified route."""
        self._validate_route(route)
        # Set the new route;
        self.current_route = route

    # Todo - Need to test that this works with the new _call position of _historise_route().
    def go_back(self) -> None:
        """Returns the current route to the previous route in the route history."""
        self.current_route = self._route_history.pop()

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    @property
    def terminal_width(self) -> int:
        return configs.terminal_width_chars

    def quit(self):
        self._quit = True
