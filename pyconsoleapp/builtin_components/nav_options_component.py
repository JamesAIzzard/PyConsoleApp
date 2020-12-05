from typing import Callable, Optional, TYPE_CHECKING

from pyconsoleapp import Component, Responder, PrimaryArg, styles

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
        self._on_back = on_back
        self._on_quit = on_quit
        self._get_current_route = get_current_route
        self._custom_back: Optional[Callable[[], None]] = None

        self.configure(responders=[
            Responder(self._on_back, args=[
                PrimaryArg(name='back', accepts_value=False, markers=['-back'])
            ]),
            Responder(self._on_quit, args=[
                PrimaryArg(name='quit', accepts_value=False, markers=['-quit'])
            ])
        ])

    def printer(self, **kwds) -> str:
        return self._template.format(
            current_route=styles.fore(self._get_current_route().replace('.', '>'), 'blue')
        )

    def _on_back(self) -> None:
        """Calls and resets custom back (if set) otherwise calls standard back function."""
        if self._custom_back is not None:
            self._custom_back()
            self._custom_back = None
        else:
            self._on_back()

    def _on_quit(self) -> None:
        """Calls quit function."""
        self._on_quit()

    def configure(self, custom_go_back: Optional[Callable[[], None]] = None, **kwds):
        """Configures the nav bar instance."""

        if custom_go_back is not None:
            self._custom_back = custom_go_back

        super().configure(**kwds)
