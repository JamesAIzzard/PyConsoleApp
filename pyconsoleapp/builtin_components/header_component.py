from typing import TYPE_CHECKING

from pyconsoleapp import Component, builtin_components

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


class HeaderComponent(Component):
    """Page Header. Includes title bar, navigation bar and message bar."""

    _template = u'''{title_bar}
{nav_bar}
{single_hr}
{message_bar}'''

    def __init__(self, app: 'ConsoleApp', **kwds):
        """
        args:
            app (ConsoleApp): Application reference, required to access app-level attributes like
                navigation and title.
        keywords:
            go_back (Callable[[], None]): Function to call when user calls 'back'
            error_message (str): Error message to show once on next render cycle.
            info_message (str): Info message to show once on next render cycle.
        """
        super().__init__(**kwds)
        self._title_bar = self.use_component(builtin_components.TitleBarComponent(app, **kwds))
        self._nav_options = self.use_component(builtin_components.NavOptionsComponent(app, **kwds))
        self._message_bar = self.use_component(builtin_components.MessageBarComponent(**kwds))
        self.configure(**kwds)

    def printer(self, **kwds) -> str:
        return self._template.format(
            title_bar=self._title_bar.printer(),
            nav_bar=self._nav_options.printer(),
            single_hr=self.single_hr,
            message_bar=self._message_bar.printer()
        )

    def configure(self, **kwds):
        """Configures the header component instance.
        keywords:
            go_back (Callable[[], None]): Function to call when user calls 'back'
            error_message (str): Error message to show once on next render cycle.
            info_message (str): Info message to show once on next render cycle.
        """
        self._title_bar.configure(**kwds)
        self._nav_options.configure(**kwds)
        self._message_bar.configure(**kwds)
        super().configure(**kwds)
