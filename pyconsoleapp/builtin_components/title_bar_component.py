from pyconsoleapp import styles, Component

_view_template = '''{app_name} | {route}
'''


class TitleBarComponent(Component):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def print_view(self) -> str:
        """Returns title bar component view as string."""
        return _view_template.format(
            app_name=styles.weight(self._app.name, 'bright'),
            route=styles.fore(self._app.current_route.replace('.', '>'), 'blue')
        )
