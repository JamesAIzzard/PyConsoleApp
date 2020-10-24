from pyconsoleapp import Component, PrimaryArg


class NavOptionsComponent(Component):
    _template = u'''Navigate Back   \u2502 -back, -b
Quit            \u2502 -quit, -q'''

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.configure(responders=[
            self.configure_responder(self._on_back, args=[
                PrimaryArg(name='back', accepts_value=False, markers=['-back', '-b'])
            ]),
            self.configure_responder(self._on_quit, args=[
                PrimaryArg(name='quit', accepts_value=False, markers=['-quit', '-q'])
            ])
        ])

    def printer(self, **kwds) -> str:
        return self._template

    def _on_back(self) -> None:
        route_list = self.app.current_route.split('.')
        if len(route_list) > 1:
            route_list.pop(-1)
            back_route = '.'.join(route_list)
            self.app.go_to(back_route)

    def _on_quit(self) -> None:
        self.app.quit()
