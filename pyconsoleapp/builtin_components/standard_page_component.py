from typing import Optional

from pyconsoleapp import Component, styles
from pyconsoleapp.builtin_components import HeaderComponent

_template_with_title = '''{header}
{page_title}
{page_title_underline}
{page_content}
>>> '''
_template_without_title = '''{header}
{page_content}
>>> '''


class StandardPageComponent(Component):
    """Standard page, including header bar and input arrows >>>. Content is passed into print_view()"""

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._page_title: Optional[str] = None
        self._header_component = self._use_component(HeaderComponent)

    def print_view(self, page_content: str) -> str:
        """Returns the standard page component view as a string, with the page content inserted."""
        # Populate the correct template and return;
        if self._page_title:
            return _template_with_title.format(
                header=self._header_component.print_view(),
                page_title=styles.weight(self._page_title, 'bright'),
                page_title_underline=len(self._page_title) * '\u2500',
                page_content=page_content)
        elif not self._page_title:
            return _template_without_title.format(
                header=self._header_component.print_view(),
                page_content=page_content)

    def configure(self, page_title: Optional[str], **kwds) -> None:
        """Sets the page title."""
        self._page_title = page_title
        super().configure(**kwds)
