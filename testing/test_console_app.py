from unittest import TestCase
from typing import Callable

from pyconsoleapp import ConsoleApp, ConsoleAppComponent, exceptions

class TestProcessResponse(TestCase):
    def setUp(self):
        self.app = ConsoleApp('Test App')
        self.test_component = ConsoleAppComponent(self.app)
        self.app._cached_components['test_component'] = self.test_component

    def test_writes_error_msg_if_no_responder_matches(self):
        self.test_component.configure_responder(Callable, args=[
            self.test_component.configure_std_primary_arg('alpha', ['-alpha'])
        ])
        self.assertEqual(self.app.error_message, None)
        self.app._process_response('Nothing matches.')
        self.assertEqual(self.app.error_message, 'This response isn\'t recognised.')