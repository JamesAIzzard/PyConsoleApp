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
    def value(self) -> Any:
        """Returns the argument's value."""
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        """Sets the argument's value, via any registered validators."""
        # First check we aren't trying to set an arbitrary value on a valueless arg;
        if not self.accepts_value and not isinstance(value, bool):
            raise ValueError('Valuess args should only be given boolean values.')
        # Now use the validators to set the value;
        temp_value = value
        for validator in self._validators:
            temp_value = validator(temp_value)
        self._value = temp_value

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

    def __init__(self, name: str, accepts_value: bool,
                 markers: Optional[List[str]] = None,
                 validators: Optional[List[Callable[..., Any]]] = None,
                 default_value: Any = None,
                 **kwds):
        super().__init__(name=name, accepts_value=accepts_value, markers=markers, validators=validators,
                         default_value=default_value, **kwds)


class OptionalArg(ResponderArg):
    """Represents an optional Responder argument."""

    def __init__(self, name: str, accepts_value: bool,
                 markers: Optional[List[str]] = None,
                 validators: Optional[List[Callable[..., Any]]] = None,
                 default_value: Any = None,
                 **kwds):
        super().__init__(name=name, accepts_value=accepts_value, markers=markers, validators=validators,
                         default_value=default_value, **kwds)
