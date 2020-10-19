import abc
from typing import List, Callable, Optional, Any


class ResponderArg(abc.ABC):
    """Base class for an argument, representing its markers, validation and default value."""

    def __init__(self, name: str, markers: Optional[List[str]] = None,
                 validators: Optional[List[Callable[..., ...]]] = None,
                 default_value: Any = None,
                 **kwds):
        self._name: str = name
        self._markers: List[str] = markers if markers is not None else []
        self._validators: List[Callable[..., ...]] = validators if validators is not None else []
        self._default_value = default_value
        # Validate the default value;
        for validator in self._validators:
            self._default_value = validator(default_value)

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
