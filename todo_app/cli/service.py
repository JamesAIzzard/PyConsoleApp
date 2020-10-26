from pyconsoleapp import ResponseValidationError
from todo_app import service, exceptions


def validate_importance_score(value) -> int:
    """Raises a ResponseValidationError if the score is invalid, otherwise returns the score as an int."""
    try:
        value = service.validate_importance_score(value)
    except exceptions.InvalidImportanceScore:
        raise ResponseValidationError('Invalid importance score.')
    return value
