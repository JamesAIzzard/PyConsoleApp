import abc
from typing import List, Callable, Optional, Any

from pyconsoleapp import exceptions


class ResponderArg(abc.ABC):
    """Base class for an argument, representing its markers, validation and default value."""

    def __init__(self, name: str, accepts_value: bool,
                 markers: Optional[List[str]] = None,
                 validators: Optional[List[Callable[..., Any]]] = None,
                 default_value: Any = None,
                 **kwds):

        if accepts_value is False:
            if validators is not None or default_value is not None:
                raise exceptions.InvalidArgConfigError

        self._name: str = name
        self._accepts_value = accepts_value
        self._markers: List[str] = markers if markers is not None else []
        self._validators: List[Callable[..., Any]] = validators if validators is not None else []
        self._value: Any = None
        self._value_buffer = []

        # If we accept a value and have a default, set the value as default (using validators in setter).
        if accepts_value is True and default_value is not None:
            self.value = default_value
        # If we don't accept a value;
        elif accepts_value is False:
            # Valuless values start at False;
            self.value = False

    @property
    def name(self) -> str:
        """Returns the argument's name."""
        return self._name

    @property
    def is_primary(self) -> bool:
        """Returns True/False to indicate if the argument is primary."""
        return isinstance(self, PrimaryArg)

    @property
    def value(self) -> Any:
        """Returns the argument's value."""
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        """Sets the argument's value, via any registered validators."""
        # First check we aren't trying to set an arbitrary value on a valueless arg;
        if not self.accepts_value and not isinstance(value, bool):
            raise ValueError('Valueless args should only be given boolean values.')
        # Now use the validators to set the value;
        temp_value = value
        for validator in self._validators:
            temp_value = validator(temp_value)
        self._value = temp_value

    def buffer_value(self, value_fragment: Any) -> None:
        """Adds the value fragment to the value buffer."""
        # Raise exception if we try and buffer a valueless arg;
        if not self._accepts_value:
            raise exceptions.OrphanValueError(value_fragment)

        self._value_buffer.append(value_fragment)

    def write_value_buffer(self) -> None:
        """Concatenates the value buffer and submits it for validation via the value setter."""
        # If writing valueless, check no args in buffer and write True;
        if not self._accepts_value and len(self._value_buffer) == 0:
            self.value = True
        # If writing valued arg, check buffer is not empty and write buffer. Raise an exception if we get an
        # empty buffer on a primary valued arg;
        elif self._accepts_value:
            if len(self._value_buffer) > 0:
                self.value = ' '.join(self._value_buffer)
            elif self.is_primary:
                raise exceptions.ArgMissingValueError('{arg_name}'.format(arg_name=self.name.replace('_', ' ')))
        # Either way, clear the buffer;
        self._value_buffer = []

    @property
    def accepts_value(self) -> bool:
        """Returns True/False to indicate if the argument can be given a value."""
        return self._accepts_value

    @property
    def markers(self) -> List[str]:
        """Returns a list of the argument's markers."""
        return self._markers

    @property
    def is_markerless(self) -> bool:
        """Returns True/False to indicate if this arg has any markers."""
        if len(self._markers):
            return False
        else:
            return True


class PrimaryArg(ResponderArg):
    """Represents a mandatory Responder argument."""

    def __init__(self, **kwds):
        super().__init__(**kwds)


class OptionalArg(ResponderArg):
    """Represents an optional Responder argument."""

    def __init__(self, **kwds):
        super().__init__(**kwds)
