from typing import TYPE_CHECKING

from pyconsoleapp import Component
from todo_app import service

if TYPE_CHECKING:
    from pyconsoleapp.builtin_components import StandardPageComponent


class TodoDashComponent(Component):
    _template = u'''There are currently {todo_count} todo items.
'''

    def __init__(self, standard_page_component: 'StandardPageComponent', **kwds):
        super().__init__(**kwds)
        self.page_component = self.use_component(standard_page_component)
        self.page_component.configure(page_title='Dashboard')

    def printer(self, **kwds) -> str:
        return self.page_component.printer(
            page_content=self._template.format(todo_count=service.count_todos()))

    def configure(self, **kwds) -> None:
        self.page_component.configure(**kwds)
