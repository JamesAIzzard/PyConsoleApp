from typing import Callable, TYPE_CHECKING

from pyconsoleapp import GuardComponent, builtin_components

if TYPE_CHECKING:
    pass


class TodoSaveCheckComponent(GuardComponent, builtin_components.YesNoDialogComponent):
    def __init__(self, todo_has_changed: Callable[[], bool], save: Callable[[], None], **kwds):
        super().__init__(message='Save changes to this todo?', **kwds)
        self._todo_has_changed: Callable[[], bool] = todo_has_changed
        self._save: Callable[[], None] = save

    def printer(self, **kwds) -> str:
        return super().printer(**kwds)

    def activated(self) -> bool:
        return self._todo_has_changed()

    def _on_yes(self) -> None:
        # Save and disable the guard.
        self._save()
        self.configure(enabled=False)

    def _on_no(self) -> None:
        # Disable the guard.
        self.configure(enabled=False)

    def configure(self, **kwds) -> None:
        super().configure(**kwds)
