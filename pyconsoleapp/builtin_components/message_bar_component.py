from textwrap import fill

from pyconsoleapp import Component, configs, styles


class MessageBarComponent(Component):
    def __init__(self, app):
        super().__init__(app)

    def printer(self, **kwds) -> str:
        output = ''
        if self.app.error_message:
            output = output+'/!\\ Error:\n{}\n'.format(
                fill(self.app.error_message, configs.terminal_width_chars)
            )
            output = styles.fore(output, 'red')
            output = output+('-'*configs.terminal_width_chars)+'\n'
            self.app.error_message = None
        if self.app.info_message:
            output = output+'[i] Info:\n{}\n'.format(
                fill(self.app.info_message, configs.terminal_width_chars)
            )
            output = styles.fore(output, 'blue')
            output = output+('-'*configs.terminal_width_chars)+'\n'
            self.app.info_message = None
        return output
