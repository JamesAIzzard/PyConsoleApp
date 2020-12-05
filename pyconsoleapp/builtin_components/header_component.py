from typing import TYPE_CHECKING

from pyconsoleapp import Component

if TYPE_CHECKING:
    from pyconsoleapp.builtin_components import TitleBarComponent, NavOptionsComponent, MessageBarComponent


class HeaderComponent(Component):
    """Page Header. Includes title bar, navigation bar and message bar."""

    _template = u'''{title_bar}
{nav_bar}
{single_hr}
{message_bar}'''

    def __init__(self, title_bar_component: 'TitleBarComponent',
                 nav_options_component: 'NavOptionsComponent',
                 message_bar_component: 'MessageBarComponent', **kwds):
        super().__init__(**kwds)
        self._title_bar = self.use_component(title_bar_component)
        self._nav_options = self.use_component(nav_options_component)
        self._message_bar = self.use_component(message_bar_component)

    def printer(self, **kwds) -> str:
        return self._template.format(
            title_bar=self._title_bar.printer(),
            nav_bar=self._nav_options.printer(),
            single_hr=self.single_hr,
            message_bar=self._message_bar.printer()
        )

    def configure(self, **kwds):
        """Configures the header component instance."""
        super().configure(**kwds)
