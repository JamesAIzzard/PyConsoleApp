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

        self.title_bar_component = title_bar_component
        self.nav_options_component = nav_options_component
        self.message_bar_component = message_bar_component

    def printer(self, **kwds) -> str:
        return self.__class__._template.format(
            title_bar=self.title_bar_component.printer(),
            nav_bar=self.nav_options_component.printer(),
            single_hr=self.single_hr,
            message_bar=self.message_bar_component.printer()
        )

    def configure(self, **kwds):
        """Configures the header component instance."""
        self.title_bar_component.configure(**kwds)
        self.nav_options_component.configure(**kwds)
        self.message_bar_component.configure(**kwds)
        super().configure(**kwds)
