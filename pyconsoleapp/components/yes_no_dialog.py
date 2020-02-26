from pyconsoleapp.console_app_component import ConsoleAppComponent
from typing import Dict

_TEMPLATE = '''
{message}
{space}(y)es / (n)o?{space}
'''

class YesNoDialog(ConsoleAppComponent):

    def __init__(self):
        self.data:Dict = {}

    def run(self):
        output = _TEMPLATE.format(
            message = self.data['message'],
            space = int((self.app.terminal_width_chars-13)/2)*''
        )
        output = self.run_parent('standard_page', output)
        return output

yes_no_dialog = YesNoDialog()