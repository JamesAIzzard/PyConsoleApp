from typing import List

import todo_app
from todo_app.todo import Todo

todos: List['Todo'] = []


def save_todo(todo: 'Todo') -> None:
    """Stubs in save functionality of a database."""
    todo.saved = True


def validate_todo_num(num) -> int:
    """Validates and returns the todo_ number."""
    try:
        num = int(num)
    except ValueError:
        raise todo_app.exceptions.InvalidTodoNumError
    if num > len(todos):
        raise todo_app.exceptions.InvalidTodoNumError
    return num


def validate_importance_score(score) -> int:
    """Validates and returnes the importance score."""
    try:
        score = int(score)
    except ValueError:
        raise todo_app.exceptions.InvalidImportanceScore
    if score < 1 or score > 3:
        raise todo_app.exceptions.InvalidImportanceScore
    return score


def add_todo(text: str, today: bool, importance: int) -> None:
    """Instantiates and adds a todo_ to the list."""
    todos.append(Todo(text=text, today=today, importance=importance))


def remove_todo(todo_num: int) -> None:
    """Removes a the todo_ associated with the specifed number."""
    todos.pop(todo_num - 1)


def fetch_todo(todo_num: int) -> 'Todo':
    """Returns the _todo at the specified index."""
    return todos[todo_num - 1]


def count_todos() -> int:
    """Returns the number of _todo items."""
    return len(todos)
