from unittest import TestCase
from typing import Callable, Union, Any

from pyconsoleapp import ConsoleApp, ConsoleAppComponent, exceptions
from pyconsoleapp.components import Responder


class TestResponder(TestCase):
    def setUp(self):
        self.app = ConsoleApp('Test App')
        self.test_component = ConsoleAppComponent(self.app)

    def test_multiple_markerless_args_raises_exception(self):
        with self.assertRaises(exceptions.DuplicateMarkerlessArgError):
            r = Responder(self.app, Callable, args=[
                self.test_component.configure_markerless_primary_arg('alpha'),
                self.test_component.configure_markerless_primary_arg('beta')
            ])

    def test_no_primary_args_raises_exception(self):
        with self.assertRaises(exceptions.NoPrimaryArgError):
            r = Responder(self.app, Callable, args=[
                self.test_component.configure_std_option_arg(
                    'alpha', ['-alpha', '-a']),
                self.test_component.configure_std_option_arg(
                    'beta', ['-beta', '-b'])
            ])

    def test_primary_marker_clashes_raise_exception(self):
        with self.assertRaises(exceptions.DuplicatePrimaryMarkerError):
            r = Responder(self.app, Callable, args=[
                self.test_component.configure_std_primary_arg(
                    'alpha', ['-alpha', '-a']),
                self.test_component.configure_std_primary_arg(
                    'beta', ['-alpha', '-b'])
            ])


class TestCheckResponseMatch(TestCase):
    def setUp(self):
        self.app = ConsoleApp('Test App')
        self.test_component = ConsoleAppComponent(self.app)

    def test_works_with_std_args(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg(
                'alpha', ['-alpha', '-a']),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b'])
        ])
        self.assertTrue(r.check_marker_match('-alpha -b'))
        self.assertFalse(r.check_marker_match('-not any markers'))
        self.assertFalse(r.check_marker_match('-a not all markers'))

    def test_works_with_valueless_args(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_valueless_primary_arg(
                'alpha', ['-alpha', '-a']),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b'])
        ])
        self.assertTrue(r.check_marker_match('-alpha -b'))
        self.assertFalse(r.check_marker_match('-not any markers'))
        self.assertFalse(r.check_marker_match('-a not all markers'))

    def test_works_with_markerless_args(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_markerless_primary_arg('alpha'),
        ])
        self.assertTrue(r.check_marker_match(
            'anything at all because its markerless'))

    def test_works_with_std_and_markerless_args(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_markerless_primary_arg('alpha'),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b'])
        ])
        self.assertTrue(r.check_marker_match(
            'anything at all because its markerless -beta'))
        self.assertFalse(r.check_marker_match(
            'anything at all because its markerless'))


class TestParseResponseToArgs(TestCase):
    def setUp(self):
        self.app = ConsoleApp('Test App')
        self.test_component = ConsoleAppComponent(self.app)

    def validate_integer(self, value: Any) -> int:
        try:
            value = int(value)
        except ValueError:
            raise exceptions.ResponseValidationError(
                '{} is not an integer.'.format(value))
        return value

    def validate_is_one(self, value: int) -> int:
        if value == 1:
            return value
        else:
            raise exceptions.ResponseValidationError(
                '{} is not the number one.'.format(value))

    def test_parses_std_primary_arg_correctly(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg(
                'alpha', ['-alpha', '-a']),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b']),
        ])
        args = r.parse_response_to_args('-alpha test alpha -b test beta')
        self.assertEqual(args['alpha'], 'test alpha')
        self.assertEqual(args['beta'], 'test beta')

    def test_validates_std_primary_arg(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg('alpha', ['-alpha', '-a'], validators=[
                self.validate_integer,
                self.validate_is_one
            ]),
            self.test_component.configure_std_primary_arg(
                'beta', ['-beta', '-b']),
        ])
        with self.assertRaises(exceptions.ResponseValidationError):
            args = r.parse_response_to_args('-alpha 2 alpha -b test beta')
        args = r.parse_response_to_args('-alpha 1 -b test beta')
        self.assertEqual(args['alpha'], 1)
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

    def test_validates_std_option_arg(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg(
                'alpha', ['-alpha', '-a']),
            self.test_component.configure_std_primary_arg('beta', ['-beta', '-b'], validators=[
                self.validate_integer, self.validate_is_one]),
        ])
        with self.assertRaises(exceptions.ResponseValidationError):
            args = r.parse_response_to_args('-alpha 2 alpha -b 2')
        args = r.parse_response_to_args('-alpha 1 -b 1')
        self.assertEqual(args['alpha'], '1')
        self.assertEqual(args['beta'], 1)

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

    def test_validates_markerless_primary_arg(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_markerless_primary_arg('alpha', validators=[
                self.validate_integer, self.validate_is_one]),
            self.test_component.configure_std_option_arg(
                'beta', ['-beta', '-b'])
        ])
        with self.assertRaises(exceptions.ResponseValidationError):
            args = r.parse_response_to_args('2 -b 2')
        args = r.parse_response_to_args('1 -b 1')
        self.assertEqual(args['alpha'], 1)
        self.assertEqual(args['beta'], '1')

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

    def test_validates_markerless_option_arg(self):
        r = Responder(self.app, Callable, args=[
            self.test_component.configure_std_primary_arg(
                'alpha', ['-alpha', '-a']),
            self.test_component.configure_markerless_option_arg('beta', validators=[
                self.validate_integer, self.validate_is_one]),
        ])
        with self.assertRaises(exceptions.ResponseValidationError):
            args = r.parse_response_to_args('2 -alpha 2 alpha')
        args = r.parse_response_to_args('1 -alpha 1 -b 1')
        self.assertEqual(args['alpha'], '1 -b 1')
        self.assertEqual(args['beta'], 1)

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
