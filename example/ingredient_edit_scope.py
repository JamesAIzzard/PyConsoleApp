from typing import Optional, TYPE_CHECKING

from pinjector import inject

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp

ingredient_name:Optional[str] = None
app:'ConsoleApp' = inject('cli.app')

def update_ingredient_display():
    app.set_window_text('Updated')
    app.show_text_window()