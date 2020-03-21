from typing import Any, Dict, List, TYPE_CHECKING
from pyconsoleapp.utility_service import utility_service
if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp
    from pyconsoleapp.utility_service import UtilityService

# class ScopedData():
#     def __init__(self, data_in_scope:Dict[str, Any], rdb:'RoutedDatabase'):
#         self.__dict__['_data'] = data_in_scope
#         self.__dict__['_rdb'] = rdb

#     def __getattribute__(self, name: str) -> Any:
#         return super().__getattribute__(name)

#     def __setattr__(self, name: str, value: Any) -> None:
#         print('setting')

class RoutedDatabase():

    def __init__(self, app):
        # Define props using __dict__ so we can override __setattr__
        # for db accessing later;
        self.__dict__['_app'] = app
        self.__dict__['_utility_service'] = utility_service        
        self.__dict__['_data'] = {}

    def __setattr__(self, name: str, value: Any) -> None:
        if not self._selected_route_key in self._data.keys():
            self._data[self._selected_route_key] = {}
        self._data[self._selected_route_key].update({name: value})

    def __getattr__(self, name: str) -> Any:
        return self._scoped_data[name]

    def __call__(self, route:List[str])->'RoutedDatabase':
        return self

    @property
    def _scoped_data(self)->Dict[str, Any]:
        data_in_scope = {}
        for route_key in self._data.keys():
            if self.is_in_scope(route_key):
                data_in_scope.update(self._data[route_key])
        return data_in_scope

    @property
    def _selected_route(self)->List[str]:
        return self._app.route

    @property
    def _selected_route_key(self)->str:
        return self._utility_service.stringify_route(self._selected_route)

    def is_in_scope(self, route_key:str)->bool:
        if route_key in self._selected_route_key:
            return True
        else:
            return False



