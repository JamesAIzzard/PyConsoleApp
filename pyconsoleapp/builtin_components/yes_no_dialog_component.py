import abc
from typing import Callable

from pyconsoleapp import Component, Responder, ResponderArg


class YesNoDialogComponent(Component, abc.ABC):
    _template = u'''{hr}
{message}
Yes \u2502 -y, -yes
No  \u2502 -n, -no
{hr}
'''

    def __init__(self, message: str, on_yes: Callable[[], None], on_no: Callable[[], None], **kwds):
        super().__init__(**kwds)
        self.message: str = message
        self._on_yes_ = on_yes
        self._on_no_ = on_no

        self.configure(responders=[
            Responder(self._on_yes_, args=[
                ResponderArg(name='yes', accepts_value=False, markers=['-yes', '-y'])
            ]),
            Responder(self._on_no_, args=[
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
