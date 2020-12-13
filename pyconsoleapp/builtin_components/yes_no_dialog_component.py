import abc

from pyconsoleapp import Component, Responder, ResponderArg


class YesNoDialogComponent(Component, abc.ABC):
    _template = u'''{hr}
{message}
Yes \u2502 -y, -yes
No  \u2502 -n, -no
{hr}
'''

    def __init__(self, message: str, **kwds):
        super().__init__(**kwds)
        self.message: str = message

        self.configure(responders=[
            Responder(self._on_yes, args=[
                ResponderArg(name='yes', accepts_value=False, markers=['-yes', '-y'])
            ]),
            Responder(self._on_no, args=[
                ResponderArg(name='no', accepts_value=False, markers=['-no', '-n'])
            ])
        ])

    def printer(self, **kwds) -> str:
        return self._template.format(
            hr=self.single_hr,
            message=self.message
        )

    @abc.abstractmethod
    def _on_yes(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _on_no(self) -> None:
        raise NotImplementedError
