class Todo:
    def __init__(self, text: str, today=False, importance=1):
        self.text: str = text
        self.today: bool = today
        self.importance: int = importance

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
