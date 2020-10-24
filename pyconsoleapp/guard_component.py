import abc
from typing import TYPE_CHECKING

from pyconsoleapp import Component

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


class GuardComponent(Component, abc.ABC):
    """Base class for all application guard components."""
    def __init__(self, app: 'ConsoleApp', **kwds):
        super().__init__(app=app, **kwds)


