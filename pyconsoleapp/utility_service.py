import re
from typing import List

def pascal_to_snake(text:str)->str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text) 
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower() 

def stringify_route(route: List[str]) -> str:
    s = "."
    return s.join(route)

def listify_route(route: str) -> List[str]:
    return route.split(".")        
