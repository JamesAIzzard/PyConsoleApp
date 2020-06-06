from unittest import TestCase

from pyconsoleapp import parse_tools


class TestParseLetterAndInteger(TestCase):

    def test_parses_correctly(self):
        letter, integer = parse_tools.parse_letter_and_integer('p1')
        self.assertEqual(letter, 'p')
        self.assertEqual(integer, 1)
        letter, integer = parse_tools.parse_letter_and_integer('a12')
        self.assertEqual(letter, 'a')
        self.assertEqual(integer, 12)
        letter, integer = parse_tools.parse_letter_and_integer('a 12')
        self.assertEqual(letter, 'a')
        self.assertEqual(integer, 12)

    def test_catches_broken_string(self):
        with self.assertRaises(parse_tools.LetterIntegerParseError):
            parse_tools.parse_letter_and_integer('')
        with self.assertRaises(parse_tools.LetterIntegerParseError):
            parse_tools.parse_letter_and_integer('  ')
        with self.assertRaises(parse_tools.LetterIntegerParseError):
            parse_tools.parse_letter_and_integer('1')


class TestParseNumberAndText(TestCase):

    def test_parses_correctly(self):
        output = parse_tools.parse_number_and_text('4kg')
        self.assertEqual(output, (4, 'kg'))