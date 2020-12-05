from pyconsoleapp import styles, Component


class TitleBarComponent(Component):
    _template = '''{title} | {tagline}'''

    def __init__(self, title: str, tagline: str, **kwds):
        super().__init__(**kwds)
        self._title = title
        self._tagline = tagline

    def printer(self, **kwds) -> str:
        """Returns title bar component view as string."""
        return self._template.format(
            name=styles.weight(self._title, 'bright'),
            tagline=self._tagline
        )
