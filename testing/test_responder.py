from unittest import TestCase

from pyconsoleapp import ConsoleApp, PrimaryArg
from pyconsoleapp.responder import Responder


class TestParseResponse(TestCase):
    def setUp(self) -> None:
        self.app = ConsoleApp('Test App')  # Dummy app to pass to responders.
        self.func = lambda: None  # Dummy function to pass to responders.

    def test_parses_std_primary_args_correctly(self):
        r = Responder(self.app, self.func, args=[
            PrimaryArg(name='alpha', accepts_value=True, markers=['-alpha', '-a']),
            PrimaryArg(name='beta', accepts_value=True, markers=['-beta', '-b'])
        ])
        args = r._parse_response('-alpha test alpha -b test beta')
        self.assertEqual(args['alpha'], 'test alpha')
        self.assertEqual(args['beta'], 'test beta')

    def test_missing_std_primary_arg_raises_exception(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg(
                'alpha', ['-alpha', '-a']),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b'])
        ])
        with self.assertRaises(exceptions.ArgMissingValueError):
            args = r.parse_response_to_args('-alpha test alpha test beta')

        with self.assertRaises(exceptions.ArgMissingValueError):
            args = r.parse_response_to_args('-alpha -beta test beta')

    def test_missing_std_primary_arg_gets_default(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg(
                'alpha', ['-alpha', '-a'], default_value='alpha'),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b'])
        ])
        args = r.parse_response_to_args('-alpha -beta test beta')
        self.assertEqual(args['alpha'], 'alpha')
        self.assertEqual(args['beta'], 'test beta')

    def test_parses_std_option_arg_correctly(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg(
                'alpha', ['-alpha', '-a']),
            self.test_component.configure_std_option_arg(
                'beta', ['-beta', '-b']),
            self.test_component.configure_std_option_arg('gamma', ['-gamma'])
        ])
        args = r.parse_response_to_args('-alpha test alpha -b test beta')
        self.assertEqual(args['alpha'], 'test alpha')
        self.assertEqual(args['beta'], 'test beta')
        self.assertEqual(args['gamma'], None)

    def test_missing_std_option_arg_is_ok(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg(
                'alpha', ['-alpha', '-a']),
            self.test_component.configure_std_option_arg(
                'beta', ['-beta', '-b'])
        ])
        args = r.parse_response_to_args('-alpha test alpha test')
        self.assertEqual(args['alpha'], 'test alpha test')
        self.assertEqual(args['beta'], None)
        args = r.parse_response_to_args('-alpha test alpha test -beta')
        self.assertEqual(args['alpha'], 'test alpha test')
        self.assertEqual(args['beta'], None)

    def test_missing_std_option_arg_gets_default(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg(
                'alpha', ['-alpha', '-a']),
            self.test_component.configure_std_option_arg(
                'beta', ['-beta', '-b'], default_value='b-value')
        ])
        args = r.parse_response_to_args('-alpha test alpha test')
        self.assertEqual(args['alpha'], 'test alpha test')
        self.assertEqual(args['beta'], 'b-value')
        args = r.parse_response_to_args('-alpha test alpha test -beta')
        self.assertEqual(args['alpha'], 'test alpha test')
        self.assertEqual(args['beta'], 'b-value')

    def test_parses_markerless_primary_arg_correctly(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_markerless_primary_arg('alpha'),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b'])
        ])
        args = r.parse_response_to_args('Some random input -b beta value')
        self.assertEqual(args['alpha'], 'Some random input')
        self.assertEqual(args['beta'], 'beta value')

    def test_missing_markerless_primary_args_gets_default(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_markerless_primary_arg(
                'alpha', default_value='a-value'),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b'])
        ])
        args = r.parse_response_to_args('-b beta value')
        self.assertEqual(args['alpha'], 'a-value')
        self.assertEqual(args['beta'], 'beta value')

    def test_missing_primary_markerless_raises_exception(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_markerless_primary_arg('alpha'),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b']),
            self.test_component.configure_valueless_option_arg('gamma', [
                '-gamma'])
        ])
        with self.assertRaises(exceptions.ArgMissingValueError):
            args = r.parse_response_to_args('')
        with self.assertRaises(exceptions.ArgMissingValueError):
            args = r.parse_response_to_args('-beta b-value')

    def test_parses_markerless_option_arg_correctly(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg(
                'alpha', ['-alpha', '-a']),
            self.test_component.configure_markerless_option_arg('beta')
        ])
        args = r.parse_response_to_args('Some random input -a a-value')
        self.assertEqual(args['alpha'], 'a-value')
        self.assertEqual(args['beta'], 'Some random input')

    def test_missing_markerless_option_args_gets_default(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_markerless_option_arg(
                'alpha', default_value='a-value'),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b'])
        ])
        args = r.parse_response_to_args('-b beta value')
        self.assertEqual(args['alpha'], 'a-value')
        self.assertEqual(args['beta'], 'beta value')

    def test_missing_markerless_option_args_gets_none(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_markerless_option_arg('alpha'),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b'])
        ])
        args = r.parse_response_to_args('-b beta value')
        self.assertEqual(args['alpha'], None)
        self.assertEqual(args['beta'], 'beta value')

    def test_valueless_primary_arg_gets_true(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_valueless_primary_arg('alpha', [
                '-alpha']),
            self.test_component.configure_std_option_arg('beta', ['-beta'])
        ])
        args = r.parse_response_to_args('-alpha -beta b-value')
        self.assertEqual(args['alpha'], True)
        self.assertEqual(args['beta'], 'b-value')

    def test_missing_valueless_primary_arg_raises_exception(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_valueless_primary_arg('alpha', [
                '-alpha']),
            self.test_component.configure_std_option_arg('beta', ['-beta'])
        ])
        with self.assertRaises(exceptions.ArgMissingValueError):
            args = r.parse_response_to_args('-beta b-value')

    def test_orphan_value_for_valueless_primary_arg_raises_exception(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_valueless_primary_arg('alpha', [
                '-alpha']),
            self.test_component.configure_std_option_arg('beta', ['-beta'])
        ])
        with self.assertRaises(exceptions.OrphanValueError):
            args = r.parse_response_to_args('-alpha a-value -beta b-value')

    def test_valueless_option_arg_gets_true(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_valueless_primary_arg('alpha', [
                '-alpha']),
            self.test_component.configure_valueless_option_arg('beta', [
                '-beta'])
        ])
        args = r.parse_response_to_args('-alpha -beta')
        self.assertEqual(args['alpha'], True)
        self.assertEqual(args['beta'], True)

    def test_missing_valueless_option_arg_gets_false(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_valueless_primary_arg('alpha', [
                '-alpha']),
            self.test_component.configure_valueless_option_arg('beta', [
                '-beta'])
        ])
        args = r.parse_response_to_args('-alpha')
        self.assertEqual(args['alpha'], True)
        self.assertEqual(args['beta'], False)

    def test_orphan_value_for_valueless_option_arg_raises_exception(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_valueless_primary_arg('alpha', [
                '-alpha']),
            self.test_component.configure_valueless_option_arg('beta', [
                '-beta'])
        ])
        with self.assertRaises(exceptions.OrphanValueError):
            args = r.parse_response_to_args('-alpha -beta b-value')
