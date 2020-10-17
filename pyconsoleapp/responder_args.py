import abc


class ResponderArg(abc.ABC):
    """Represents an argument associated with a Responder."""
    def __init__(self, **kwds):
        ...

class PrimaryArg(ResponderArg):
    """Represents a mandatory Responder argument."""

class OptionalArg(ResponderArg):
    """Represents an optional Responder argument."""