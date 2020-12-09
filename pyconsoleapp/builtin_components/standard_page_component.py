from typing import Optional, Callable, TYPE_CHECKING

from pyconsoleapp import Component, styles

if TYPE_CHECKING:
    from pyconsoleapp.builtin_components import HeaderComponent


class StandardPageComponent(Component):
    """Standard page, including header bar and input arrows >>>."""

    _template_with_title = '''{header}
{page_title}
{page_title_underline}
{page_content}
>>> '''
    _template_without_title = '''{header}
{page_content}
>>> '''

    def __init__(self, header_component: 'HeaderComponent', **kwds):
        super().__init__(**kwds)
        self._page_title: Optional[str] = None
        self._header_component = self.use_component(header_component)

    def printer(self, page_content: str, **kwds) -> str:
        """Returns the standard page component view as a string, with the page content inserted."""
        # Populate the correct template and return;
        if self._page_title:
            return self._template_with_title.format(
                header=self._header_component.printer(),
                page_title=styles.weight(self._page_title, 'bright'),
                page_title_underline=len(self._page_title) * '\u2500',
                page_content=page_content)
        elif not self._page_title:
            return self._template_without_title.format(
                header=self._header_component.printer(),
                page_content=page_content)

    def configure(self, page_title: Optional[str] = None, **kwds) -> None:
        """Configures the StandardPageComponent instance."""
        if page_title is not None:
            self._page_title = page_title
        self._header_component.configure(**kwds)
        super().configure(**kwds)
