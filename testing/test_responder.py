from unittest import TestCase

from pyconsoleapp import ConsoleApp, PrimaryArg, OptionalArg, validators, exceptions
from pyconsoleapp.responder import Responder


class TestParseResponse(TestCase):
    """Tests response parsing.
    Note:
        At this point, the response has already been confirmed to match the responder,
        so passing responses which do not match the responder will raise unhandled errors,
        and is beyond the scope of these tests.
    """

    def setUp(self) -> None:
        self.app = ConsoleApp('Test App')  # Dummy app to pass to responders.
        self.func = lambda: None  # Dummy function to pass to responders.
        self.marker_names = ["alpha", "beta", "gamma"]
        self.markers = ["-alpha", "-beta", "-gamma"]
        self.s_values = ["alpha val", "beta val", "gamma val"]
        self.i_values = [1, 2, 3]

    def build_response(self, keystring: str) -> str:
        chunks = keystring.split('-')
        response = ''
        piece = ''
        for chunk in chunks:
            if chunk[0] == 'm':
                piece = self.markers[int(chunk[1])]
            elif chunk[0] == 'v':
                if chunk[1] == 's':
                    piece = self.s_values[int(chunk[2])]
                elif chunk[1] == 'i':
                    piece = self.i_values[int(chunk[2])]
            response = '{} {}'.format(response, piece)
        return response

    def argname(self, ref: int) -> str:
        """Returns marker name."""
        return self.marker_names[ref]

    def m(self, ref: int) -> str:
        """Returns marker."""
        return self.markers[ref]

    def sval(self, ref: int) -> str:
        """Returns string value."""
        return self.s_values[ref]

    def ival(self, ref: int) -> int:
        """Returns int value."""
        return self.i_values[ref]

    def test_std_primary_args_basic_function_single_arg(self):
        response = self.build_response('m0-vs0')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=[self.m(0)])
        ])
        correct_args = {
            self.argname(0): self.sval(0)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_std_primary_args_basic_function_double_arg(self):
        response = self.build_response('m1-vs1-m2-vi2')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(1), accepts_value=True, markers=[self.m(1)]),
            PrimaryArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)], validators=[
                validators.validate_integer
            ])
        ])
        correct_args = {
            self.argname(1): self.sval(1),
            self.argname(2): self.ival(2)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_std_primary_args_single_arg_missing_val(self):
        response = self.build_response('m0')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=[self.m(0)])
        ])
        with self.assertRaises(exceptions.ArgMissingValueError):
            _ = responder._parse_response(response)

    def test_std_primary_args_double_arg_error_one_missing_val(self):
        response = self.build_response('m0-vs0-m1')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=[self.m(0)]),
            PrimaryArg(name=self.argname(1), accepts_value=True, markers=[self.m(1)])
        ])
        with self.assertRaises(exceptions.ArgMissingValueError):
            _ = responder._parse_response(response)
        # Try the other way around
        response = self.build_response('m0-m1-vs1')
        with self.assertRaises(exceptions.ArgMissingValueError):
            _ = responder._parse_response(response)

    def test_one_option_arg_basic_function(self):
        response = self.build_response('m0-vs0-m2-vs2')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=[self.m(0)]),
            OptionalArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)])
        ])
        correct_args = {
            self.argname(0): self.sval(0),
            self.argname(2): self.sval(2)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_ok_to_miss_optional_arg(self):
        response = self.build_response('m0-vs0')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=[self.m(0)]),
            OptionalArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)])
        ])
        correct_args = {
            self.argname(0): self.sval(0),
            self.argname(2): None
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_missing_optional_arg_gets_default(self):
        response = self.build_response('m0-vs0')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=[self.m(0)]),
            OptionalArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)], default_value=self.sval(2))
        ])
        correct_args = {
            self.argname(0): self.sval(0),
            self.argname(2): self.sval(2)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_optional_arg_marker_without_val_raises_error(self):
        response = self.build_response('m0-vs0-m1')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=[self.m(0)]),
            OptionalArg(name=self.argname(1), accepts_value=True, markers=[self.m(1)])
        ])
        with self.assertRaises(exceptions.ArgMissingValueError):
            _ = responder._parse_response(response)

    def test_optional_arg_marker_without_val_raises_error_even_with_default(self):
        response = self.build_response('m0-vs0-m1')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=[self.m(0)]),
            OptionalArg(name=self.argname(1), accepts_value=True, markers=[self.m(1)], default_value=self.sval(1))
        ])
        with self.assertRaises(exceptions.ArgMissingValueError):
            _ = responder._parse_response(response)

    def test_markerless_primary_arg_basic_function(self):
        response = self.build_response('vs0')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=None)
        ])
        correct_args = {
            self.argname(0): self.sval(0)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_markerless_primary_with_marker_primary_basic_function(self):
        response = self.build_response('vs0-m1-vs1')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=None),
            PrimaryArg(name=self.argname(1), accepts_value=True, markers=[self.m(1)])
        ])
        correct_args = {
            self.argname(0): self.sval(0),
            self.argname(1): self.sval(1)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_markerless_primary_raises_exception_if_missing_without_default(self):
        response = self.build_response('m1-vs1')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=None),
            PrimaryArg(name=self.argname(1), accepts_value=True, markers=[self.m(1)])
        ])
        with self.assertRaises(exceptions.ArgMissingValueError):
            _ = responder._parse_response(response)

    def test_markerless_primary_gets_default_if_missing(self):
        response = self.build_response('m1-vs1')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(0), accepts_value=True, markers=None, default_value=self.sval(0)),
            PrimaryArg(name=self.argname(1), accepts_value=True, markers=[self.m(1)])
        ])
        correct_args = {
            self.argname(0): self.sval(0),
            self.argname(1): self.sval(1)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_markerless_option_basic_function(self):
        response = self.build_response('m2-vs2')
        responder = Responder(self.app, self.func, args=[
            OptionalArg(name=self.argname(1), accepts_value=True, markers=None),
            PrimaryArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)])
        ])
        correct_args = {
            self.argname(1): None,
            self.argname(2): self.sval(2)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_markerless_option_gets_default(self):
        response = self.build_response('m2-vs2')
        responder = Responder(self.app, self.func, args=[
            OptionalArg(name=self.argname(1), accepts_value=True, markers=None, default_value=self.sval(1)),
            PrimaryArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)])
        ])
        correct_args = {
            self.argname(1): self.sval(1),
            self.argname(2): self.sval(2)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_valueless_primary_with_value_raises_exception(self):
        response = self.build_response('m1-vs1-m2-vs2')
        responder = Responder(self.app, self.func, args=[
            PrimaryArg(name=self.argname(1), accepts_value=False, markers=[self.m(1)]),
            PrimaryArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)])
        ])
        with self.assertRaises(exceptions.OrphanValueError):
            _ = responder._parse_response(response)

    def test_valueless_optional_with_value_raises_exception(self):
        response = self.build_response('m1-vs1-m2-vs2')
        responder = Responder(self.app, self.func, args=[
            OptionalArg(name=self.argname(1), accepts_value=False, markers=[self.m(1)]),
            PrimaryArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)])
        ])
        with self.assertRaises(exceptions.OrphanValueError):
            _ = responder._parse_response(response)

    def test_valueless_optional_gets_false_when_not_present(self):
        response = self.build_response('m2-vs2')
        responder = Responder(self.app, self.func, args=[
            OptionalArg(name=self.argname(1), accepts_value=False, markers=[self.m(1)]),
            PrimaryArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)])
        ])
        correct_args = {
            self.argname(1): False,
            self.argname(2): self.sval(2)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_valueless_optional_gets_true_when_present(self):
        response = self.build_response('m1-m2-vs2')
        responder = Responder(self.app, self.func, args=[
            OptionalArg(name=self.argname(1), accepts_value=False, markers=[self.m(1)]),
            PrimaryArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)])
        ])
        correct_args = {
            self.argname(1): True,
            self.argname(2): self.sval(2)
        }
        parsed_args = responder._parse_response(response)
        self.assertEqual(parsed_args, correct_args)

    def test_error_when_default_on_valueless_arg(self):
        # Not strictly parse related but included for completeness.
        with self.assertRaises(exceptions.InvalidArgConfigError):
            responder = Responder(self.app, self.func, args=[
                OptionalArg(name=self.argname(1), accepts_value=False, markers=[self.m(1)], default_value=True),
                PrimaryArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)])
            ])
        with self.assertRaises(exceptions.InvalidArgConfigError):
            responder = Responder(self.app, self.func, args=[
                PrimaryArg(name=self.argname(1), accepts_value=False, markers=[self.m(1)], default_value=True),
                PrimaryArg(name=self.argname(2), accepts_value=True, markers=[self.m(2)])
            ])
