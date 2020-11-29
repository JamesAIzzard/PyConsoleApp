from typing import Callable, Optional, TYPE_CHECKING

from pyconsoleapp import Component, Responder, PrimaryArg

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


class NavOptionsComponent(Component):
    """Navigation bar. Includes quit and back options."""
    _template = u'''Navigate Back   \u2502 -back, -b
Quit            \u2502 -quit, -q'''

    def __init__(self, app: 'ConsoleApp', **kwds):
        super().__init__(**kwds)
        self._app: 'ConsoleApp' = app
        self._on_back_: Optional[Callable[[], None]] = None

        self.configure(responders=[
            Responder(self._on_back, args=[
                PrimaryArg(name='back', accepts_value=False, markers=['-back', '-b'])
            ]),
            Responder(self._on_quit, args=[
                PrimaryArg(name='quit', accepts_value=False, markers=['-quit', '-q'])
            ])
        ])

    def printer(self, **kwds) -> str:
        return self._template

    def _on_back(self) -> None:
        if self._on_back_ is not None:
            self._on_back_()
        else:
            route_list = self._app.current_route.split('.')
            if len(route_list) > 1:
                route_list.pop(-1)
                back_route = '.'.join(route_list)
                self._app.go_to(back_route)

    def _on_quit(self) -> None:
        self._app.quit()

    def configure(self, go_back: Optional[Callable[[], None]] = None, **kwds):
        """Configures the nav bar instance."""

        if go_back is not None:
            self._on_back_ = go_back

        super().configure(**kwds)
