import abc
from typing import Callable, Optional

from pyconsoleapp import Component


class GuardComponent(Component, abc.ABC):
    """Base class for all application guard components."""

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._should_activate: Callable[[], bool] = lambda: True
        self._enabled: bool = True

    @property
    def activated(self) -> bool:
        """Returns True/False to indicate if the guard is activated."""
        return self._should_activate()

    @property
    def enabled(self) -> bool:
        """Returns True/False to indicate if the guard is enabled."""
        return self._enabled

    def configure(self, should_activate: Optional[Callable[[], bool]] = None,
                  enabled: Optional[bool] = None, **kwds) -> None:
        if should_activate is not None:
            self._should_activate = should_activate
        if enabled is not None:
            self._enabled = enabled
        super().configure(**kwds)
