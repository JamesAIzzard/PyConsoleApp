from typing import Callable, List, TYPE_CHECKING

from pyconsoleapp import exceptions

if TYPE_CHECKING:
    from pyconsoleapp.responder_args import ResponderArg


class Responder:
    """Associates a function with a list of arguments."""

    def __init__(self, func: Callable[..., None], args: List['ResponderArg'], **kwds):
        self._func: Callable[..., None] = func
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
