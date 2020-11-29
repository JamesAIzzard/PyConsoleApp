from typing import TYPE_CHECKING

from pyconsoleapp import styles, Component

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


class TitleBarComponent(Component):
    _template = '''{app_name} | {route}'''

    def __init__(self, app: 'ConsoleApp', **kwds):
        super().__init__(**kwds)
        self._app: 'ConsoleApp' = app

    def printer(self, **kwds) -> str:
        """Returns title bar component view as string."""
        return self._template.format(
            app_name=styles.weight(self._app.name, 'bright'),
            route=styles.fore(self._app.current_route.replace('.', '>'), 'blue')
        )
