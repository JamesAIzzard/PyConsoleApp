from typing import List, Any

from singleton_decorator import singleton
import pyconsoleapp as pcap

from example import todo

def validate_importance_score(importance: str) -> None:
    # Check importance score is within allowable range;
    imp = int(importance)
    if imp < 1 or imp > 3:
        raise pcap.ResponseValidationError('The importance score must be between 1-3.')   

@singleton
class TodoService():
    def __init__(self):
        self._todos:List['todo.Todo'] = []

    @property
    def todos(self) -> List['todo.Todo']:
        return self._todos

    def add_todo(self, text:str, today:bool, importance:int)->None:
        # Create a todo instance;
        t = todo.Todo(text, today, importance)
        # Append to list;
        self._todos.append(t)

    def remove_todo(self, todo_num:int)->None:
        # Remove the todo;
        self.todos.pop(todo_num-1)

    def fetch_todo(self, todo_num:int) -> 'todo.Todo':
        # Return the todo;
        return self.todos[todo_num-1]

    def validate_todo_num(self, todo_num:str)->int:
        try:
            tn = int(todo_num)
        except TypeError:
            raise pcap.ResponseValidationError('{todo_num} does not refer to a current todo.'.format(todo_num=todo_num))
        # Check the integer refers to a todo on the current list;
        if tn > len(self.todos) or tn < 1:
            raise pcap.ResponseValidationError('{todo_num} does not refer to a current todo.'.format(todo_num=todo_num))
        return tn
