from typing import TYPE_CHECKING

from pyconsoleapp import Component, builtin_components

if TYPE_CHECKING:
    from pyconsoleapp.builtin_components import TitleBarComponent, NavOptionsComponent, MessageBarComponent


class HeaderComponent(Component):
    """Page Header. Includes title bar, navigation bar and message bar."""

    _template = u'''{title_bar}
{nav_bar}
{single_hr}
{message_bar}'''

    def __init__(self, **kwds):
        super().__init__(**kwds)

        if 'title_bar_component' in kwds:
            self._title_bar_component = kwds['title_bar_component']
        else:
            self._title_bar_component = builtin_components.TitleBarComponent(**kwds)

        if 'nav_options_component' in kwds:
            self._nav_options_component = kwds['nav_options_component']
        else:
            self._nav_options_component = builtin_components.NavOptionsComponent(**kwds)

        if 'message_bar_component' in kwds:
            self._message_bar_component = kwds['message_bar_component']
        else:
            self._message_bar_component = MessageBarComponent(**kwds)

    def printer(self, **kwds) -> str:
        return self.__class__._template.format(
            title_bar=self._title_bar_component.printer(),
            nav_bar=self._nav_options_component.printer(),
            single_hr=self.single_hr,
            message_bar=self._message_bar_component.printer()
        )

    def configure(self, **kwds):
        """Configures the header component instance."""
        self._title_bar_component.configure(**kwds)
        self._nav_options_component.configure(**kwds)
        self._message_bar_component.configure(**kwds)
        super().configure(**kwds)
