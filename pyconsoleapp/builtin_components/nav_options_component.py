from pyconsoleapp import Component, Responder, PrimaryArg, OptionalArg

_template = u'''Navigate Back   \u2502 -back, -b
Quit            \u2502 -quit, -q
'''


class NavOptionsComponent(Component):

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._configure_state('main', responders=[
            Responder(self._on_back, args=[PrimaryArg('back flag', markers=['-back', '-b'])]),
            Responder(self._on_quit, args=[PrimaryArg('quit flag', markers=['-quit', '-q'])])
        ])

    @staticmethod
    def print_view(self) -> str:
        return _template

    def _on_back(self) -> None:
        route_list = self._app.current_route.split('.')
        if len(route_list) > 1:
            route_list.pop(-1)
            back_route = '.'.join(route_list)
            self._app.go_to(back_route)

    def _on_quit(self) -> None:
        self._app.quit()
