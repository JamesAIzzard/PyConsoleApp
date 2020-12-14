from typing import TYPE_CHECKING

import todo_app
from pyconsoleapp import Component, builtin_components

if TYPE_CHECKING:
    from pyconsoleapp.builtin_components import HeaderComponent


class TodoDashComponent(Component):
    _template = u'''There are currently {todo_count} todo items.
'''

    def __init__(self, header_component: 'HeaderComponent', **kwds):
        super().__init__(**kwds)
        self.page_component = self.use_component(
            builtin_components.StandardPageComponent(header_component=header_component, page_title='Dashboard'))

    def printer(self, **kwds) -> str:
        return self.page_component.printer(
            page_content=self._template.format(todo_count=todo_app.service.count_todos()))

    def configure(self, **kwds) -> None:
        super().configure(**kwds)
        self.page_component.configure(**kwds)
