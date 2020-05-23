from typing import TYPE_CHECKING
from unittest import TestCase

import pyconsoleapp # run module __init__ to configure DI;
from pinjector import inject

if TYPE_CHECKING:
    from pyconsoleapp import utilities

class TestParseLetterAndInteger(TestCase):
    def setUp(self):
        self.ut:'utilities' = inject('pyconsoleapp.utilities')

    def test_parses_correctly(self):
        letter, integer = self.ut.parse_letter_and_integer('p1')
        self.assertEqual(letter, 'p')
        self.assertEqual(integer, 1)
        letter, integer = self.ut.parse_letter_and_integer('a12')
        self.assertEqual(letter, 'a')
        self.assertEqual(integer, 12)   
        letter, integer = self.ut.parse_letter_and_integer('a 12')
        self.assertEqual(letter, 'a')
        self.assertEqual(integer, 12)                         

    def test_catches_broken_string(self):
        with self.assertRaises(ValueError):
            self.ut.parse_letter_and_integer('')
        with self.assertRaises(ValueError):
            self.ut.parse_letter_and_integer('  ')  
        with self.assertRaises(ValueError):
            self.ut.parse_letter_and_integer('1')  

class TestParseNumberAndText(TestCase):
    def setUp(self):
        self.ut: 'utilities' = inject('pyconsoleapp.utilities')

    def test_parses_correctly(self):
        output = self.ut.parse_number_and_text('4kg')
        self.assertEqual(output, (4, 'kg'))                     