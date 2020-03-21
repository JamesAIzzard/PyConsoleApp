from typing import Any, Dict, List, TYPE_CHECKING
from pyconsoleapp.utility_service import utility_service
if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp

class RoutedDatabase():

    def __init__(self, app:'ConsoleApp'):
        # Define props using __dict__ so we can override __setattr__
        # for db accessing later;
        self.__dict__['_app'] = app
        self.__dict__['_selected_route'] = None
        self.__dict__['_utility_service'] = utility_service        
        self.__dict__['_data'] = {}

    def __setattr__(self, name: str, value: Any) -> None:
        if not self._selected_route_key in self._data.keys():
            self._data[self._selected_route_key] = {}
        self._data[self._selected_route_key].update({name: value})

    def __getattr__(self, name: str) -> Any:
        if name in self._scoped_data.keys():
            return self._scoped_data[name]
        else:
            return None

    def __call__(self, route:List[str])->'RoutedDatabase':
        route = self._app.complete_relative_route(route)
        self.__dict__['_selected_route'] = route
        return self

    @property
    def _scoped_data(self)->Dict[str, Any]:
        data_in_scope = {}
        for route_key in self._data.keys():
            if self.is_parent_of_selected(route_key):
                data_in_scope.update(self._data[route_key])
        return data_in_scope

    @property
    def _selected_route_key(self)->str:
        return self._utility_service.stringify_route(self._selected_route)

    def is_parent_of_selected(self, route_key:str)->bool:
        if route_key in self._selected_route_key:
            return True
        else:
            return False

    def is_child_of_selected(self, route_key:str)->bool:
        if self._selected_route_key in route_key:
            return True
        else:
            return False

    def clear(self):
        for route_key in self._data.keys():
            if self.is_child_of_selected(route_key):
                self._data[route_key] = {}



