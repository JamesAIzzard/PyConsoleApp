from typing import Optional, TYPE_CHECKING

from pyconsoleapp import Component, builtin_components

if TYPE_CHECKING:
    from pyconsoleapp.builtin_components import TitleBarComponent, NavOptionsComponent, MessageBarComponent


class HeaderComponent(Component):
    """Page Header. Includes title bar, navigation bar and message bar."""

    _template = u'''{title_bar}
{nav_bar}
{single_hr}
{message_bar}'''

    def __init__(self, title: Optional[str] = None,
                 tagline: Optional[str] = None,
                 title_bar_component: Optional['TitleBarComponent'] = None,
                 nav_options_component: Optional['NavOptionsComponent'] = None,
                 message_bar_component: Optional['MessageBarComponent'] = None, **kwds):
        super().__init__(**kwds)
        if title_bar_component is None:
            title_bar_component = builtin_components.TitleBarComponent(title, tagline)
        self._title_bar_component = self.use_component(title_bar_component)
        self._nav_options = self.use_component(nav_options_component)
        self._message_bar = self.use_component(message_bar_component)

    def printer(self, **kwds) -> str:
        return self.__class__._template.format(
            title_bar=self._title_bar.printer(),
            nav_bar=self._nav_options.printer(),
            single_hr=self.single_hr,
            message_bar=self._message_bar.printer()
        )

    def configure(self, **kwds):
        """Configures the header component instance."""
        self._title_bar.configure(**kwds)
        self._nav_options.configure(**kwds)
        self._message_bar.configure(**kwds)
        super().configure(**kwds)
