from typing import Any, Dict, List

class RouteData():
    
    def __init__(self):
        self._parents:List[RouteData] = []
        self._data:Dict[str, Any]

    def __setattr__(self, name: str, value: Any) -> None:
        self._data[name] = value

    def __getattr__(self, name:str)->Any:
        # First look for data locally;
        if name in self._data.keys():
            return self._data[name]
        # The look through each child's data;
        for parent in self._parents:
            if hasattr(parent, name):
                return getattr(parent, name)
        # Raise exception if not found;
        raise AttributeError('The attribute {} was not found in the route data'.\
            format(name))
