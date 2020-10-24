from typing import Callable, List, Dict, Any, Optional, TYPE_CHECKING

from pyconsoleapp import exceptions, responder_args

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pyconsoleapp.responder_args import ResponderArg


class Responder:
    """Associates a function with a list of arguments."""

    def __init__(self, app: 'ConsoleApp', func: Callable[..., None], args: Optional[List['ResponderArg']] = None,
                 **kwds):
        self._app: 'ConsoleApp' = app
        self._responder_func: Callable[..., None] = func
        self._args: List['ResponderArg'] = args if args is not None else []

        self._markerless_arg: Optional['ResponderArg'] = None
        for arg in self._args:
            if arg.is_markerless:
                if self._markerless_arg is None:
                    self._markerless_arg = arg
                else:
                    raise exceptions.DuplicateMarkerlessArgError

        super().__init__(**kwds)

    @property
    def has_markerless_arg(self) -> bool:
        """Returns True/False to indicate if any constituent args are markerless."""
        return self._markerless_arg is not None

    @property
    def markerless_arg(self) -> Optional['ResponderArg']:
        """Returns the responder's markerless arg, if exists, otherwise returns None."""
        return self._markerless_arg

    @property
    def has_marker_args(self) -> bool:
        """Returns True/False to indicate if any constituent args have markers."""
        if self.has_markerless_arg:
            return len(self._args) > 1
        else:
            return len(self._args) > 0

    @property
    def is_argless(self) -> bool:
        """Returns True/False to indicate if the responder is argless."""
        return len(self._args) == 0

    @property
    def _primary_args(self) -> List['ResponderArg']:
        """Returns a list of the primary arguments assigned to this responder."""
        primary_args = []
        for arg in self._args:
            if isinstance(arg, responder_args.PrimaryArg):
                primary_args.append(arg)
        return primary_args

    @property
    def _args_and_values(self) -> Dict[str, Any]:
        """Returns a dictionary of all arg names and their current values."""
        kwds = {}
        for arg in self._args:
            kwds[arg.name] = arg.value
        return kwds

    def check_marker_match(self, response: str) -> bool:
        """Returns True/False to indicate if the given response matches this responder."""
        split_response = set(response.split())
        for arg in self._primary_args:
            if len(split_response.intersection(set(arg.markers))) == 0:
                return False
        return True

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Splits the response into into its respective arguments.
        Note: Validation occurs here, in the argument setters."""

        words = response.split()  # Split the response into a list of words.
        current_arg = self.markerless_arg  # None if no markerless arg exists.
        value_buffer = []  # List used to compile words for a value.

        # Cycle through each word in the response;
        for word in words:
            word_is_marker = False
            for arg in self._args:
                word_is_marker = word in arg.markers

                # If we found a marker, finalise the previous value if exists, and reset the buffer;
                if word_is_marker:
                    current_arg = arg
                    if len(value_buffer):
                        current_arg.value = ' '.join(value_buffer)
                    value_buffer = []

                    # If the arg is valueless, adjust value to indicate it was found;
                    if not arg.accepts_value:
                        arg.value = True
                        current_arg = None

                    break  # Found, so stop searching args.

            # Append value if not a marker, and an arg is collecting a value;
            if word_is_marker is False:
                # If we are getting a value before a marker, it is an orphan;
                if current_arg is None:
                    raise exceptions.OrphanValueError('Unexpected argument: {}'.format(word))
                # Append the word to the value buffer;
                value_buffer.append(word)

        # Out of words, so write the final value buffer;
        if len(value_buffer):
            current_arg.value = ' '.join(value_buffer)

        # Return the kwds dict;
        return self._args_and_values

    def respond(self, response: Optional[str] = None) -> None:
        """Calls the function associated with the responder, passing any parsed arguments, if present."""
        self._app.stop_responding()  # Stop by default, and the function can then restart before next loop.
        if response is None:
            self._responder_func()
        else:
            kwds = self._parse_response(response)
            self._responder_func(**kwds)
