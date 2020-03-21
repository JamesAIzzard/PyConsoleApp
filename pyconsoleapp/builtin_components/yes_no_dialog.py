from ..console_app_component import ConsoleAppComponent
from typing import Optional

_TEMPLATE = '''
{message}
{space}(y)es / (n)o?{space}
'''

class YesNoDialog(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self.message:Optional[str] = None

    def print(self):
        output = _TEMPLATE.format(
            message = self.message,
            space = int((self.app.configs.terminal_width_chars-13)/2)*''
        )
        output = self.app.get_component('StandardPage').print(output)
        return output
