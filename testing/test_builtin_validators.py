from unittest import TestCase

from pyconsoleapp import builtin_validators, exceptions

class TestParseLetterAndInteger(TestCase):

    def test_parses_correctly(self):
        letter, integer = builtin_validators.validate_letter_and_integer('p1')
        self.assertEqual(letter, 'p')
        self.assertEqual(integer, 1)
        letter, integer = builtin_validators.validate_letter_and_integer('a12')
        self.assertEqual(letter, 'a')
        self.assertEqual(integer, 12)
        letter, integer = builtin_validators.validate_letter_and_integer('a 12.0')
        self.assertEqual(letter, 'a')
        self.assertEqual(integer, 12)

    def test_catches_broken_string(self):
        with self.assertRaises(exceptions.ResponseValidationError):
            builtin_validators.validate_letter_and_integer('')
        with self.assertRaises(exceptions.ResponseValidationError):
            builtin_validators.validate_letter_and_integer('  ')
        with self.assertRaises(exceptions.ResponseValidationError):
            builtin_validators.validate_letter_and_integer('1')

class TestParseLetterAndFloat(TestCase):

    def test_parses_correctly(self):
        letter, number = builtin_validators.validate_letter_and_float('i20.5')
        self.assertEqual(letter, 'i')
        self.assertEqual(number, 20.5)
        letter, number = builtin_validators.validate_letter_and_float('i 20.5')
        self.assertEqual(letter, 'i')
        self.assertEqual(number, 20.5)    

    def test_catches_broken_string(self):
        with self.assertRaises(exceptions.ResponseValidationError):
            builtin_validators.validate_letter_and_float('')
        with self.assertRaises(exceptions.ResponseValidationError):
            builtin_validators.validate_letter_and_float('  ')
        with self.assertRaises(exceptions.ResponseValidationError):
            builtin_validators.validate_letter_and_float('1')            

class TestParseNumberAndText(TestCase):

    def test_parses_correctly(self):
        output = builtin_validators.validate_number_and_text('4kg')
        self.assertEqual(output, (4, 'kg'))
                     
