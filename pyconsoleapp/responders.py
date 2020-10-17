from typing import Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pyconsoleapp.responder_args import ResponderArg


class Responder:
    """Associates a function with a list of arguments."""

    def __init__(self, func: Callable[..., None], args: List['ResponderArg'], **kwds):
        self._func: Callable[..., None] = func
        self._args: List['ResponderArg'] = args
        super().__init__(**kwds)


class ArglessResponder(Responder):
    """Associates a function with an empty response."""

    def __init__(self, func: Callable[..., None], **kwds):
        super().__init__(func=func, args=[], **kwds)