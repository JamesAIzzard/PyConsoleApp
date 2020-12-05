from typing import Optional

from pyconsoleapp import Component, styles


class MessageBarComponent(Component):
    """Component to display the info and error messages stored on the component."""
    _main_template = '''{content}
{hr}\n'''
    _info_template = '[i] Info: {message}'
    _error_template = '/!\\ Error: {message}'

    def __init__(self, info_message: Optional[str] = None, error_message: Optional[str] = None, **kwds):
        super().__init__(**kwds)
        self._error_message: Optional[str] = info_message
        self._info_message: Optional[str] = error_message

    def set_error_message(self, message: str) -> None:
        """Sets the component's error message."""
        if self._error_message.replace(' ', '') == '':
            message = "An error occurred."
        self._error_message = message

    def set_info_message(self, message: str) -> None:
        """Sets the component's info message."""
        self._info_message = message

    def printer(self, **kwds) -> str:
        if self._error_message is not None:
            message = self._error_message  # Reset the error message;
            self._error_message = None
            return self._main_template.format(
                content=styles.fore(self._error_template.format(message=message), 'red'),
                hr=self.single_hr
            )
        elif self._info_message is not None and not self._info_message.replace(' ', '') == '':
            message = self._info_message
            self._info_message = None  # Reset the info message;
            return self._main_template.format(
                content=styles.fore(self._info_template.format(message=message), 'blue'),
                hr=self.single_hr
            )
        else:
            return ''
