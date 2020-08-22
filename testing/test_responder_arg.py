from unittest import TestCase

from pyconsoleapp import ConsoleApp, ConsoleAppComponent

class TestIsValueless(TestCase):
    def setUp(self) -> None:
        self.app = ConsoleApp('Test App')
        self.test_component = ConsoleAppComponent(self.app)

    def test_correctly_identifies_if_valueless_primary(self) -> None:
        ra = self.test_component.configure_valueless_primary_arg('tester', markers=['-tester'])
        self.assertTrue(ra.is_valueless)

    def test_correctly_identifies_if_valueless_option(self) -> None:
        ra = self.test_component.configure_valueless_option_arg('tester', markers=['-tester'])
        self.assertTrue(ra.is_valueless)        

class TestIsMarkerless(TestCase):
    def setUp(self) -> None:
        self.app = ConsoleApp('Test App')
        self.test_component = ConsoleAppComponent(self.app)

    def test_correctly_identifies_if_markerless_primary(self) -> None:
        ra = self.test_component.configure_markerless_primary_arg(name='tester')
        self.assertTrue(ra.is_markerless)

    def test_correctly_identifies_if_markerless_option(self) -> None:
        ra = self.test_component.configure_markerless_option_arg(name='tester')
        self.assertTrue(ra.is_markerless)        
