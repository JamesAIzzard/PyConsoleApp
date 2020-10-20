import abc
from typing import List, Callable, Optional, Any

from pyconsoleapp import exceptions


class ResponderArg(abc.ABC):
    """Base class for an argument, representing its markers, validation and default value."""

    def __init__(self, name: str, has_value: bool,
                 markers: Optional[List[str]] = None,
                 validators: Optional[List[Callable[..., ...]]] = None,
                 default_value: Any = None,
                 **kwds):

        if has_value is False:
            if markers is not None or validators is not None or default_value is not None:
                raise exceptions.InvalidArgConfigError

        if has_value is False and default_value is not None:
            raise exceptions.InvalidArgConfigError

        self._name: str = name
        self._has_value = has_value
        self._markers: List[str] = markers if markers is not None else []
        self._validators: List[Callable[..., ...]] = validators if validators is not None else []
        self._value: ... = None
        if has_value is False:
            self._value: ... = False
        else:
            self.value = default_value  # Set the default value via the setter to run any validations.

    @property
    def value(self) -> ...:
        return self._value

    @value.setter
    def value(self, value: ...) -> None:
        temp_value = value
        for validator in self._validators:
            temp_value = validator(temp_value)
            self._value = temp_value

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
