from typing import Any, Dict, List, TYPE_CHECKING
from pyconsoleapp.utility_service import utility_service
if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp
    from pyconsoleapp.utility_service import UtilityService

class RoutedDatabase():

    def __init__(self, app):
        self._selected_route:List[str] = app.route
        self._app: 'ConsoleApp' = app
        self._utility_service:'UtilityService' = utility_service        
        self._data: Dict[str, Dict[str, Any]] = {}

    def __call__(self, route: List[str]) -> 'RoutedDatabase':
        route = self._app.complete_relative_route(route)
        self._selected_route = route
        return self

    def __setattr__(self, name: str, value: Any) -> None:
        route_key = self._utility_service.stringify_route(self._selected_route)
        # If the property is in scope;
        if self._in_scope(name):
            # Set it;
            self.__getattribute__(name) = value
        # Otherwise, create it;
        if route_key in self._data.keys():
            

    def __getattribute__(self, name:str) -> Any:
        pass

    def clear(self)->None:
        route_key = self._utility_service.stringify_route(self._selected_route)
        self._data[route_key] = 




