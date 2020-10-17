class Todo():
    def __init__(self, text:str, today=False, importance=0):
        self.text:str = text
        self.today:bool = today
        self.importance:int = importance