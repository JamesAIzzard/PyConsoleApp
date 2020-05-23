from typing import Tuple
import re


def parse_letter_and_integer(chars_to_parse: str) -> Tuple[str, int]:
    '''Parses a string whose first character is a letter, and
    whose following characters form an integer, into a tuple
    containing a letter and an integer.

    Arguments:
        chars_to_parse {str} -- Characters to parse.

    Raises:
        LetterIntegerParseError: Indicating general parse failure.

    Returns:
        Tuple[str, int] -- A tuple containing the first letter and
            following integer as its first and second items
            respectively.
    '''
    # Catch empty string;
    if chars_to_parse == '' or len(chars_to_parse) < 1:
        raise ValueError
    # Check the first char is a letter;
    letter = chars_to_parse[0]
    if not letter.isalpha():
        raise ValueError
    # Check the remaining letters are numbers;
    integer = chars_to_parse[1:]
    integer = int(integer)  # Will raise ValueError if fails;
    # Tests passed, so return the value;
    return (letter, integer)


def parse_number_and_text(qty_and_text: str) -> Tuple[float, str]:
    '''Parses a string whose first chars should be numerical and
    whose second chars should be text, Returning these two parts
    as a tuple.

    Arguments:
        qty_and_text {str} -- Input string to be parsed.

    Raises:
        ValueError: Indicating the string could not be parsed.

    Returns:
        Tuple[float, str] -- The input, separated into its text
            and numerical components.
    '''
    output = None
    # Strip any initial whitespace;
    qty_and_text = qty_and_text.replace(' ', '')
    # Work along the string until you find something which is
    # not a number;
    for i, char in enumerate(qty_and_text):
        # If char cannot be parsed as a number,
        # split the string here;
        if not char.isnumeric() and not char == '.':
            number_part = float(qty_and_text[:i])
            text_part = str(qty_and_text[i:])
            output = (number_part, text_part)
            break
    if not output:
        raise ValueError('Unable to parse {} into a number and text.'
                         .format(qty_and_text))
    # Return tuple;
    return output


def sentence_case(text: str) -> str:
    '''Capitalizes the first letter of each word in the
    text provided.

    Args:
        text (str): Text to convert to sentence case.

    Returns:
        str: Text with sentence case capitalisation.
    '''
    words_list = text.split('_')
    for word in words_list:
        word.capitalize()
    return ' '.join(words_list)
