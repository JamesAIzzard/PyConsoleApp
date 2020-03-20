from typing import Any, Dict, List, TYPE_CHECKING
from pyconsoleapp.utility_service import utility_service
if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp
    from pyconsoleapp.utility_service import UtilityService

class RouteData():

    def __init__(self):
        self._data:Dict[str, Any] = {}

    def __setattr__(self, name: str, value: Any) -> None:
        self._data[name] = value

    def __getattribute__(self, name: str) -> Any:
        return self._data[name]


class RoutedDatabase():

    def __init__(self, app):
        self._selected_route:List[str] = app.route
        self._app: 'ConsoleApp' = app
        self._utility_service:'UtilityService' = utility_service        
        self._data: Dict[str, RouteData] = {}

    def __call__(self, route: List[str]) -> 'RoutedDatabase':
        route = self._app.complete_relative_route(route)
        self._selected_route = route
        return self

    def __setattr__(self, name: str, value: Any) -> None:
        pass

    def __getattribute__(self, name:str) -> Any:
        pass

    def clear(self)->None:
        route_key = self._utility_service.stringify_route(self._selected_route)
        self._data[route_key] = 




