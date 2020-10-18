from pyconsoleapp import Component
from pyconsoleapp.builtin_components import MessageBarComponent
from pyconsoleapp.builtin_components import NavOptionsComponent
from pyconsoleapp.builtin_components import TitleBarComponent

_view_template = '''{title_bar}
{nav_bar}
{single_hr}
{message_bar}'''


class HeaderComponent(Component):
    """Page Header. Includes title bar, navigation bar and message bar."""

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._title_bar = self._use_component(TitleBarComponent)
        self._nav_options = self._use_component(NavOptionsComponent)
        self._message_bar = self._use_component(MessageBarComponent)

    def print_view(self) -> str:
        return _view_template.format(
            title_bar=self._title_bar.print_view(),
            nav_bar=self._nav_options.print_view(),
            single_hr=u'\u2500' * self._app.terminal_width,
            message_bar=self._message_bar.print_view()
        )
