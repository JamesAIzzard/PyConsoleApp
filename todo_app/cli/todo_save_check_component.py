from typing import Optional, TYPE_CHECKING

from pyconsoleapp import GuardComponent, builtin_components

from todo_app import service

if TYPE_CHECKING:
    from todo_app import Todo


class TodoSaveCheckComponent(GuardComponent, builtin_components.YesNoDialogComponent):
    def __init__(self, **kwds):
        super().__init__(
            message='Save changes to this todo?',
            **kwds
        )
        self._todo_to_check: Optional['Todo'] = None
        super().configure(should_activate=lambda: not self._todo_to_check.saved)

    def printer(self, **kwds) -> str:
        return super().printer(**kwds)

    def _on_yes(self) -> None:
        # Save and disable the guard.
        service.save_todo(self._todo_to_check)
        self.configure(should_activate=lambda: False)

    def _on_no(self) -> None:
        # Disable the guard.
        self.configure(should_activate=lambda: False)

    def configure(self, todo_to_check: Optional['Todo'] = None, **kwds) -> None:
        if todo_to_check is not None:
            self._todo_to_check = todo_to_check
        super().configure(**kwds)
