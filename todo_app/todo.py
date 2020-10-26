class Todo:
    def __init__(self, text: str, today=False, importance=1):
        self.text: str = text
        self.today: bool = today
        self.importance: int = importance
        self.saved: bool = False
