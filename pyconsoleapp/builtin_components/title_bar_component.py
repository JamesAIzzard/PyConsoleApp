from typing import Optional

from pyconsoleapp import styles, Component


class TitleBarComponent(Component):
    _template = u'''{title} | {tagline}'''

    def __init__(self, title: str, tagline: str, **kwds):
        super().__init__(**kwds)
        if title is None:
            raise
        self._title = title
        self._tagline = tagline

    def printer(self, **kwds) -> str:
        """Returns title bar component view as string."""
        return self._template.format(
            title=styles.weight(self._title, 'bright'),
            tagline=self._tagline
        )

    def configure(self, title: Optional[str] = None, tagline: Optional[str] = None, **kwds):
        if title is not None:
            self._title = title
        if tagline is not None:
            self._tagline = tagline
        super().configure(**kwds)
