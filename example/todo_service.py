from typing import List, Union

from singleton_decorator import singleton

@singleton
class TodoService():
    def __init__(self):
        self.todos:List[str] = []
        self.current_todo_index:int = 0
        self.editing:bool = False

    @property
    def selected_todo(self)->str:
        if self.editing:
            return self.todos[self.current_todo_index]
        else:
            raise AttributeError