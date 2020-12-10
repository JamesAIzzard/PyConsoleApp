from typing import Optional, TYPE_CHECKING

from pyconsoleapp import Component, builtin_components
from todo_app import service, app, title_bar_component, message_bar_component, nav_options_component, header_component

if TYPE_CHECKING:
    from pyconsoleapp.builtin_components import StandardPageComponent, NavOptionsComponent


class TodoDashComponent(Component):
    _template = u'''There are currently {todo_count} todo items.
'''

    def __init__(self, on_nav_back:Optional[Callable[[], None]]=None, **kwds):
        super().__init__(**kwds)


        if on_nav_back is not None:
            # Create new header with custom back function;
            self._header_component = builtin_components.HeaderComponent(
                title_bar_component=title_bar_component,
                message_bar_component=message_bar_component,
                nav_options_component=NavOptionsComponent()
            )
        else:
            self._header_component = header_component
        self.page_component = self.use_component(builtin_components.StandardPageComponent(**kwds))
        self.page_component.configure(page_title='Dashboard')

    def printer(self, **kwds) -> str:
        return self.page_component.printer(
            page_content=self._template.format(todo_count=service.count_todos()))

    def configure(self, **kwds) -> None:
        self.page_component.configure(**kwds)
