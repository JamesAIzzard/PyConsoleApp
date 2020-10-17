from pyconsoleapp import styles, utils
from todo_app import Todo


def format_todo(number: int, todo_item: 'Todo') -> str:
    # Make the text red if today;
    if todo_item.today:
        text = styles.fore(todo_item.text, 'red')
    else:
        text = todo_item.text
    # Build & return the string;
    return utils.wrap_text('{number}. {todo_text}'.format(
        number=styles.weight(str(number), 'bright'),
        todo_text=text))
