from typing import Callable, List, Dict, Optional, TYPE_CHECKING

from pyconsoleapp import exceptions

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pyconsoleapp.responder_args import ResponderArg


class Responder:
    """Associates a function with a list of arguments."""

    def __init__(self, app: 'ConsoleApp', func: Callable[..., None], args: Optional[List['ResponderArg']] = None,
                 **kwds):
        self._app: 'ConsoleApp' = app
        self._responder_func: Callable[..., None] = func
        self._args: Optional[List['ResponderArg']] = args

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
    def _args_and_values(self) -> Dict[str, ...]:
        """Returns a dictionary of all arg names and their current values."""
        kwds = {}
        for arg in self._args:
            kwds[arg.name] = arg.value
        return kwds

    def _parse_response(self, response: str) -> Dict[str, ...]:
        """Splits the response into into its respective arguments.
        Note: Validation occurs here, in the argument setters."""

        words = response.split()
        current_arg = self.markerless_arg  # None if no markerless arg exists.
        value_buffer = []  # List used to compile words for a value.

        # Cycle through each word in the response;
        for word in words:
            word_is_marker = False
            for arg in self._args:
                word_is_marker = word in arg.markers

                # If we found a marker, finalise the previous value if exists, and reset the buffer;
                if word_is_marker:
                    if len(value_buffer):
                        arg.value = ' '.join(value_buffer)
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
