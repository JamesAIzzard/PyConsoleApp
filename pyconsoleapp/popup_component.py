import abc
from typing import TYPE_CHECKING

from pyconsoleapp import Component

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


class PopupComponent(Component, abc.ABC):
    """A component designed for being dynamically shown regardless of current app route."""

    def __init__(self, app: 'ConsoleApp', **kwds):
        super().__init__(app, **kwds)

    def activate(self, **kwds) -> None:
        """Adds this instance to the list of active popups."""
        self._app.activate_popup(self)

    def deactivate(self, **kwds) -> None:
        """Removes self from the app's list of active popups."""
        self._app.deactivate_popup(self)
