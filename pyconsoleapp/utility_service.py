import re
from typing import List

class UtilityService():

    def pascal_to_snake(self, text:str)->str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text) 
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower() 

    def stringify_route(self, route: List[str]) -> str:
        s = ">"
        return s.join(route)

    def listify_route(self, route: str) -> List[str]:
        return route.split(">")        

utility_service = UtilityService()