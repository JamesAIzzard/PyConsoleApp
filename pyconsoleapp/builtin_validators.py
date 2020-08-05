from typing import Any

from pyconsoleapp import exceptions

def validate_integer(value:Any) -> int:
    try:
        int_value = int(value)
    except TypeError:
        raise exceptions.ResponseValidationError
    return int_value