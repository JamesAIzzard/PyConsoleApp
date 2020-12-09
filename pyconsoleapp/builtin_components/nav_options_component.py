from typing import Callable, Optional, TYPE_CHECKING

from pyconsoleapp import Component, Responder, ResponderArg, styles

if TYPE_CHECKING:
    pass


class NavOptionsComponent(Component):
    """Navigation bar. Includes quit and back options."""
    _template = u'''{current_route}
-back \u2502 Navigate back.
-quit \u2502 Close the app.
'''

    def __init__(self, on_back: Callable[[], None], on_quit: Callable[[], None],
                 get_current_route: Callable[[], str], **kwds):
        super().__init__(**kwds)
        self._on_back_ = on_back
        self._on_quit_ = on_quit
        self._get_current_route = get_current_route

        self.configure(responders=[
            Responder(self._on_back, args=[
                ResponderArg(name='back', accepts_value=False, markers=['-back']),
            ]),
            Responder(self._on_quit, args=[
                ResponderArg(name='quit', accepts_value=False, markers=['-quit'])
            ])
        ])

    def printer(self, **kwds) -> str:
        return self.__class__._template.format(
            current_route=styles.fore(self._get_current_route().replace('.', '>'), 'blue')
        )

    def _on_back(self) -> None:
        """Calls and resets custom back (if set) otherwise calls standard back function."""
        self._on_back_()

    def _on_quit(self) -> None:
        """Calls quit function."""
        self._on_quit_()

    def configure(self, on_back: Optional[Callable[[], None]] = None, **kwds):
        """Configures the nav bar instance."""

        if on_back is not None:
            self._on_back_ = on_back

        super().configure(**kwds)
