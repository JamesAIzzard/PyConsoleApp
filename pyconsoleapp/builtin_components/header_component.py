from pyconsoleapp import Component, builtin_components


class HeaderComponent(Component):
    """Page Header. Includes title bar, navigation bar and message bar."""

    _template = u'''{title_bar}
{nav_bar}
{single_hr}
{message_bar}'''

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._title_bar = self.use_component(builtin_components.TitleBarComponent)
        self._nav_options = self.use_component(builtin_components.NavOptionsComponent)
        self._message_bar = self.use_component(builtin_components.MessageBarComponent)

    def printer(self, **kwds) -> str:
        return self._template.format(
            title_bar=self._title_bar.printer(),
            nav_bar=self._nav_options.printer(),
            single_hr='\u2500' * self.app.terminal_width,
            message_bar=self._message_bar.printer()
        )
