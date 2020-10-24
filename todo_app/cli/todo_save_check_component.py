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

    def printer(self, **kwds) -> str:
        return super().printer(**kwds)

    def _on_yes(self) -> None:
        service.save_todo(self._todo_to_check)
        self.stop_guarding()

    def _on_no(self) -> None:
        self.stop_guarding()

    def configure(self, todo_to_check: Optional['Todo'] = None, **kwds) -> None:
        self._todo_to_check = todo_to_check
        super().configure(should_activate=lambda: not todo_to_check.saved, **kwds)
