from typing import Callable, List, Dict, Optional, TYPE_CHECKING

from pyconsoleapp import exceptions

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pyconsoleapp.responder_args import ResponderArg


class Responder:
    """Associates a function with a list of arguments."""

    def __init__(self, app: 'ConsoleApp', func: Callable[..., None], args: List['ResponderArg'], **kwds):
        self._app: 'ConsoleApp' = app
        self._responder_func: Callable[..., None] = func
        self._args: List['ResponderArg'] = args
        super().__init__(**kwds)

    @property
    def has_markerless_arg(self) -> bool:
        """Returns True/False to indicate if any constituent args are markerless."""
        has_markerless_arg = False
        for arg in self._args:
            if arg.is_markerless:
                if not has_markerless_arg:
                    has_markerless_arg = True
                elif has_markerless_arg:
                    raise exceptions.DuplicateMarkerlessArgError
        return False

    @property
    def has_marker_args(self) -> bool:
        """Returns True/False to indicate if any constituent args have markers."""
        if len(self._args):
            for arg in self._args:
                if not arg.is_markerless:
                    return True

    @property
    def is_argless(self) -> bool:
        """Returns True/False to indicate if the responder is argless."""
        return isinstance(self, ArglessResponder)

    def _parse_response(self, response: str) -> Dict[str, ...]:
        """Splits the response into a dictionary of *unvalidated* arg-value pairs."""

        # Place to store arg names found in the response;
        matched_arg_names: List[str] = []

        # ResponderArgs now hold their one values and run their validators automatically inside value setter.
        # values are initialised automatically too.
        # Todo - Carry on converting the old method to use this new approach.

        # Split the response into list so we can work through each word;
        words = response.split()

        # Init the first arg name;
        if self.has_markerless_arg:
            current_arg_name = self.markerless_arg.name
        else:
            current_arg_name = None

        # Now cycle through each word in the response;
        for word in words:
            # Check if the word is a marker;
            is_marker = False
            for arg in self.args:
                if word in arg.markers:
                    matched_arg_names.append(arg.name)
                    current_arg_name = arg.name
                    is_marker = True
                    # If the arg is valueless, adjust value to indicate it was found;
                    if arg.is_valueless:
                        parsed_args[arg.name] = True
                        current_arg_name = None
                    break  # Found, so stop searching args.
            # Append value if not a marker, and an arg is collecting a value;
            if not is_marker:
                # If we are getting a value before a marker, it is an orphan;
                if current_arg_name is None:
                    raise exceptions.OrphanValueError('Unexpected argument: {}'.format(word))
                # If the word is the first for this value, init;
                if parsed_args[current_arg_name] is None:
                    parsed_args[current_arg_name] = word
                # Otherwise append;
                else:
                    parsed_args[current_arg_name] = '{} {}'.format(
                        parsed_args[current_arg_name], word)

    def respond(self, response: Optional[str] = None) -> None:
        """Calls the function associated with the responder, passing any parsed arguments, if present."""
        self._app.stop_responding()  # Stop by default, and the function can then restart before next loop.
        if response is None:
            self._responder_func()
        else:
            kwds = self._parse_response(response)
            self._responder_func(kwds)


class ArglessResponder(Responder):
    """Associates a function with an empty response."""

    def __init__(self, func: Callable[..., None], **kwds):
        super().__init__(func=func, args=[], **kwds)

    @property
    def has_markerless_arg(self) -> bool:
        """Always returns False, since all argless responders have no markerless args."""
        return False

    @property
    def has_marker_args(self) -> bool:
        """Always returns False, since all argless responders have no marker args."""
        return False
