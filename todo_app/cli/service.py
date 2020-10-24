from pyconsoleapp import styles, utils, ResponseValidationError
from todo_app import Todo, service, exceptions


def format_todo_menu_item(number: int, todo_item: 'Todo') -> str:
    """Produces a formatted string summary of a numbered _todo item."""
    # Make the text red if today;
    if todo_item.today:
        text = styles.fore(todo_item.text, 'red')
    else:
        text = todo_item.text
    # Build & return the string;
    return utils.wrap_text('{number}. {todo_text}'.format(
        number=styles.weight(str(number), 'bright'),
        todo_text=text))


def validate_importance_score(value) -> int:
    """Raises a ResponseValidationError if the score is invalid, otherwise returns the score as an int."""
    try:
        value = service.validate_importance_score(value)
    except exceptions.InvalidImportanceScore:
        raise ResponseValidationError('Invalid importance score.')
    return value
