from abc import ABC
from inspect import signature
from typing import Callable, Dict, List, Tuple, Any, Optional, Union, TYPE_CHECKING, cast

from pyconsoleapp import ConsoleApp, exceptions

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


class Responder():
    def __init__(self,
                 app: 'ConsoleApp',
                 func: Callable,
                 args: List['ResponderArg']):
        self._app = app
        self._func = func
        self._args = args

    @property
    def app(self) -> 'ConsoleApp':
        return self._app

    @property
    def args(self) -> List['ResponderArg']:
        return self._args

    @property
    def is_argless_responder(self) -> bool:
        if len(self.args) == 0:
            return True
        return False

    @property
    def has_markerless_arg(self) -> bool:
        if not self.is_argless_responder:
            for arg in self.args:
                if None in arg.markers:
                    return True
        return False

    @property
    def markerless_arg(self) -> Optional['ResponderArg']:
        if self.has_markerless_arg:
            for arg in self.args:
                if arg.is_valueless:
                    return arg
        return None

    def check_response_match(self, response: str) -> bool:
        '''Returns True/False to indicate if all of the primary
        argument markers are present in the response.

        Args:
            response (str): Text entered by user.

        Returns:
            bool: To indicate match or no match.
        '''
        for arg in self.args:
            if arg.primary:
                if not arg.check_marker_match(response):
                    return False
        return True

    def parse_response_to_args(self, response: str) -> Dict[str, Any]:
        '''Converts a response into a dictionary of arguments
        corresponding to those defined for this responder.
        - Returns dict of all possible args, None if not present.
        - Valueless are assigned True if present, False if not.
        - Sequentially passes values through any validation functions.

        Args:
            response (str): [description]

        Returns:
            Dict[str, Any]: [description]
        '''

        # Init the dict with None for each value, or
        # False if arg is valueless;
        parsed_args = {}
        for arg in self.args:
            if arg.is_valueless:
                parsed_args[arg.name] = False
            else:
                parsed_args[arg.name] = None

        # Helper function to accumulate arg values;
        def add_to_arg_value(name: str, word: str) -> None:
            if parsed_args[name] == None:
                parsed_args[name] = word
            else:
                parsed_args[name] = parsed_args[name]+' {}'.format(word)

        # Work through the response, word by word and
        # pass values into the arg dict;
        words = response.split()  # Convert the response to a list of words;

        # Init the first arg name;
        if self.has_markerless_arg:
            current_arg_name = self.markerless_arg.name
        else:
            current_arg_name = None

        for word in words:  # Now cycle through each word in the response;
            # Check for matches against each arg;
            for arg in self.args:
                if word in arg.markers:
                    current_arg_name = arg.name
                    break
                elif not current_arg_name == None:
                    add_to_arg_value(current_arg_name, word)

        # TODO - Now run validation over each arg.

        return parsed_args

    def __call__(self, response: str = '') -> None:
        # Parse the response into args;
        args = self.parse_response_to_args(response)
        # Ready to go, assume stop responding after this;
        # (Component can undo this if it wants to continue the
        # response cycle).
        self._app.stop_responding()
        # Call the function, passing the args if the function expects them;
        sig = signature(self._func)
        if len(sig.parameters) > 0:
            self._func(args)
        else:
            self._func()


class ResponderArg():
    def __init__(self,
                 primary: bool,
                 name: str,
                 markers: List[Union[str, None]],
                 validators: List[Callable] = [],
                 default_value: Any = None):
        self._primary = primary
        self._name = name
        self._markers = markers
        self._validators = validators

        # TODO - Check that the default value passes the validation!

        self._default_value = default_value

    def check_marker_match(self, response: str) -> bool:
        '''Returns True/False to indicate if markers for this argument
        are present in the response.

        Args:
            response (str): Response to search for arguments.

        Returns:
            bool: To indicate if a marker was found.
        '''
        chunked_response = response.split()
        for marker in self.markers:
            if marker in chunked_response or marker == None:
                return True
        return False

    @property
    def primary(self) -> bool:
        return self._primary

    @property
    def name(self) -> str:
        return self._name

    @property
    def markers(self) -> List[Union[str, None]]:
        return self._markers

    @property
    def validators(self) -> List[Callable]:
        return self._validators

    @property
    def default_value(self) -> Any:
        return self._default_value

    @property
    def is_markerless(self) -> bool:
        if None in self.markers:
            return True
        else:
            return False

    @property
    def is_valueless(self) -> bool:
        if self.name == None:
            return True
        else:
            return False


class ConsoleAppComponent(ABC):
    def __init__(self, app: 'ConsoleApp'):
        # Stash the app reference;
        self.app = app
        # Dicts to store state specific print & responder funcs;
        self._responders: Dict[Union[None, str],
                               List['Responder']] = {None: []}
        self._printers: Dict[Union[None, str], Callable] = {}
        # Init state storage;
        self._states: List[Union[None, str]] = [None]
        self._current_state: Union[None, str] = self._states[0]

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
            # Add this component to the active components list
            self.app.activate_component(self)
        # Return whatever was requested;
        return super().__getattribute__(name)

    @property
    def name(self) -> str:
        '''Returns the name of the component.

        Returns:
            str: Component name.
        '''
        return self.__class__.__name__

    @property
    def current_state(self) -> Union[None, str]:
        return self._current_state

    @current_state.setter
    def current_state(self, value: Union[None, str]) -> None:
        self._validate_states([value])
        self._current_state = value

    @property
    def states(self) -> List[Union[None, str]]:
        return self._states

    def configure_states(self, states: List[Union[None, str]]) -> None:
        # Prevent default being overwritten by no states;
        if len(states):
            # Reset to remove the None state;
            self._states = []
            self._responders = {}
            # Assign states;
            for state in states:
                self._states.append(state)
                self._responders[state] = []
            # Init the current state as the first one;
            self.current_state = states[0]
        else:
            raise ValueError('At least one state must be provided.')

    def _validate_states(self, states: List[Union[None, str]]):
        # Check that each state in the list has been configured;
        for state in states:
            if not state in self.states:
                raise exceptions.StateNotFoundError

    @property
    def _current_print_function(self) -> Callable:
        # Error if there isn't a print function stored against the current state;
        if not self.current_state in self._printers.keys():
            raise exceptions.NoPrintFunctionError
        # Return the relevant function;
        return self._printers[self.current_state]

    def print(self, *args, **kwargs) -> Union[str, Tuple[str, str]]:
        return self._current_print_function(*args, **kwargs)

    def before_print(self) -> None:
        pass

    def configure_printer(self,
                          func: Callable,
                          states: List[Union[str, None]] = [None]) -> None:
        # Check all the states;
        self._validate_states(states)
        # Assign the print function to specified states;
        for state in states:
            self._printers[state] = func

    def configure_responder(self,
                            func: Callable,
                            states: List[Union[str, None]] = [None],
                            args: List['ResponderArg'] = []) -> None:
        '''Generic responder configuration. 

        Args:
            func (Callable): Handler function to execute when the responder is called.
            states (List[Union[str, None]]): The component states under which the responder
                can be called. Defaults to [None].
            args (List[ResponderArg]): The responder args associated with the responder.
                The contents of these args are passed to the function as a dict, when the
                responder is called. Defaults to None.
        '''
        # Check the states are valid;
        self._validate_states(states)
        # TODO - Check there are no marker clashes within this responder;
        # Create and stash the responder object in the correct states;
        r = Responder(self.app, func, args)
        for state in self.states:
            self._responders[state].append(r)

    @staticmethod
    def configure_primary_arg(name: str,
                              markers: List[Union[str, None]] = [],
                              validators: List[Callable] = [],
                              default_value: Any = None) -> 'ResponderArg':
        '''Configures a primary argument object, describing how input is collected
        and validated against an argument to be passed to the handler function.
        'Primary' indicates the argument must be present for the responder to
        match and be called. In the case where the name parameter == None, the argument
        will not contribute values to the arg dict passed to the handler function.

        Returns:
            ResponderArg
        '''
        return ResponderArg(primary=True, name=name, markers=markers,
                            validators=validators, default_value=default_value)

    @staticmethod
    def configure_markerless_primary_arg(name: str,
                                         validators: List[Callable] = [],
                                         default_value: Any = None) -> 'ResponderArg':
        '''Configures a primary argument object without a marker, i.e one whose value
        is the text entered before the first marker found in the response.

        Returns:
            ResponderArg
        '''
        return ConsoleAppComponent.configure_primary_arg(markers=[None],
                                                         name=name,
                                                         validators=validators,
                                                         default_value=default_value)

    @staticmethod
    def configure_valueless_primary_arg(name: str,
                                        markers: List[str]) -> 'ResponderArg':
        '''Configures a primary argument object which only looks for a marker and no
        additional arguments.

        Returns:
            ResponderArg
        '''
        return ConsoleAppComponent.configure_primary_arg(name=name,
                                                         markers=cast(List[Union[str, None]], markers))

    @staticmethod
    def configure_option_arg(name: str,
                             markers: List[Union[str, None]] = [],
                             validators: List[Callable] = [],
                             default_value: Any = None) -> 'ResponderArg':
        '''Configures an optional argument object, describing how input is collected
        and validated against an argument to be passed to the handler function.
        'Option' indicates the argument must be present for the responder to
        match and be called. In the case where the name parameter == None, the argument
        will not contribute values to the arg dict passed to the handler function.

        Returns:
            ResponderArg
        '''
        return ResponderArg(primary=False, name=name, markers=markers,
                            validators=validators, default_value=default_value)

    @staticmethod
    def configure_markerless_option_arg(name: str,
                                        validators: List[Callable] = [],
                                        default_value: Any = None) -> 'ResponderArg':
        '''Configures an option argument object without a marker, i.e one whose value
        is the text entered before the first marker found in the response.

        Returns:
            ResponderArg
        '''
        return ConsoleAppComponent.configure_option_arg(markers=[None], name=name,
                                                        validators=validators, default_value=default_value)

    @staticmethod
    def configure_valueless_option_arg(name: str,
                                       markers: List[str]) -> 'ResponderArg':
        '''Configures an option argument object which only looks for a marker and no
        additional arguments.

        Returns:
            ResponderArg
        '''
        return ConsoleAppComponent.configure_option_arg(name, markers=cast(List[Union[str, None]], markers))

    def configure_argless_responder(self,
                                    func: Callable,
                                    states: List[Union[str, None]] = [None]) -> None:
        '''A shortcut method to configure a responder to fire when the
        user presses enter without entering anything.

        Args:
            func (Callable): Function to call when responder is matched.
            states (List[Union[str, None]], optional): Component states from which the responder 
                can be called. Defaults to [None].
        '''
        # First check that there are no other empty responders;
        for responder in self._responders[self.current_state]:
            if responder.is_argless_responder:
                raise exceptions.DuplicateEmptyResponderError
        # Go ahead and configure a responder without args;
        self.configure_responder(func, states)

    @property
    def argless_responder(self) -> Optional['Responder']:
        '''Returns the argless responder assigned to the component,
        if it exists. If there is no argless responder configured,
        None is returned.

        Returns:
            Responder | None
        '''
        for responder in self._responders[self.current_state]:
            if responder.is_argless_responder:
                return responder
        return None

    @property
    def marker_responders(self) -> List['Responder']:
        '''Returns a list of responders whose arguments are
        each assigned a marker.

        Returns:
            List[Responder]
        '''
        marker_responders = []
        for responder in self._responders[self.current_state]:
            if not responder.is_argless_responder and not responder.has_markerless_arg:
                marker_responders.append(responder)
        return marker_responders

    @property
    def markerless_responder(self) -> Optional['Responder']:
        '''Returns the markerless responder assigned to the component,
        if it exists. If there is no markerless responder configured,
        None is returned.

        A markerless responder is a responder containing an argument
        with its marker set as None. This means it will match against
        any input preceeding the first marker found in the response.

        Returns:
            Responder | None
        '''
        for responder in self._responders[self.current_state]:
            if responder.has_markerless_arg:
                return responder
        return None


class ConsoleAppGuardComponent(ConsoleAppComponent):
    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)

    def clear_self(self):
        def search_and_clear_guard_map(guard_map):
            # Place to store guarded route to clear;
            rt_to_clear = None
            # Work through the entrance guard list looking for self;
            for route in guard_map.keys():
                # If found;
                if guard_map[route] == self:
                    # Delete entry from guard dict;
                    rt_to_clear = route
            if rt_to_clear:
                del guard_map[rt_to_clear]
        # Search and clear entrance & exit maps;
        search_and_clear_guard_map(self.app._route_entrance_guard_map)
        search_and_clear_guard_map(self.app._route_exit_guard_map)
