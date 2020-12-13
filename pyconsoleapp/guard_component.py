import abc
from typing import Callable, Optional

from pyconsoleapp import Component


class GuardComponent(Component, abc.ABC):
    """Base class for all application guard components."""

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._enabled: bool = True

    @property
    @abc.abstractmethod
    def activated(self) -> bool:
        """Returns True/False to indicate if the guard is activated."""
        raise NotImplementedError

    @property
    def enabled(self) -> bool:
        """Returns True/False to indicate if the guard is enabled."""
        return self._enabled

    def configure(self, enabled: Optional[bool] = None, **kwds) -> None:
        if enabled is not None:
            self._enabled = enabled
        super().configure(**kwds)
