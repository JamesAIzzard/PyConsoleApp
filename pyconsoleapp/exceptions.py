from typing import Optional

class PyConsoleAppError(Exception):
    pass

class NoPrintFunctionError(PyConsoleAppError):
    pass

class StateNotFoundError(PyConsoleAppError):
    pass

class SignatureClashError(PyConsoleAppError):
    pass

class DuplicateEmptyResponderError(PyConsoleAppError):
    pass

class ResponseValidationError(PyConsoleAppError):
    def __init__(self, message:Optional[str]=None):
        self.message = message

class ArgMissingValueError(ResponseValidationError):
    def __init__(self, message:Optional[str]=None):
        super().__init__(message)