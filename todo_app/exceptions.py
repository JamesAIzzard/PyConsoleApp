class TodoAppException(Exception):
    """Base exception class for the app"""


class InvalidTodoNumError(TodoAppException):
    """Indicating the number is not a valid _todo index."""


class InvalidImportanceScore(TodoAppException):
    """Indicating the importance score is invalid."""
