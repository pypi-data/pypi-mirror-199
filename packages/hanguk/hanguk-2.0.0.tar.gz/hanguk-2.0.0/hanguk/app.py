from collections.abc import Generator, Iterable, Iterator
from io import StringIO
from itertools import islice
from typing import Any, List, Tuple

import json
import os


class Hanguk:
    """A class to represent a Hanguk object.

    Parameters
    ----------
    text : str
        The text associated with the Hanguk object.

    Attributes
    ----------
    text : str
        The text associated with the Hanguk object.

    Methods
    -------
    read() -> str:
        Reads input text and maps each chunk of three characters to a corresponding value 
        in a lookup table, returning the resulting text as a string.
    stream() -> StringIO:
        A generator function that reads input text and maps each chunk of three 
        characters to a corresponding value in a lookup table.
    """

    with open(os.path.join(os.path.dirname(__file__), 'static', 'data.json'), 'r') as f:
        __DATA = json.load(f)

    def __init__(self, text: str):
        """Constructs all the necessary attributes for the Hanguk object.

        Parameters
        ----------
        text : str
            The text associated with the Hanguk object.
        """
        self.text = text

    def _jamo(self, char: str) -> Tuple[str]:
        """Returns a tuple of strings representing jamo characters for a given character.

        Parameters
        ----------
        char : str
            The character to be converted into jamo characters.

        Returns
        -------
        Tuple[str]
            A tuple of strings representing jamo characters for a given character.
        """
        # Check if the character is a valid Korean syllable in Unicode range 44032-55203
        if 44032 <= (x := ord(char)) <= 55203:
            # Calculate the index of the syllable in the Unicode block
            a = x - 44032

            # Calculate the trailing consonant
            b = a % 28

            # Calculate the vowel
            c = 1 + ((a - b) % 588) // 28

            # Calculate the leading consonant
            d = 1 + a // 588

            # Compute the Unicode codepoints for the jamo characters based on lookup table
            q = [*map(sum, zip(*[[d, c, b], [4351, 4448, 4519]]))]

            # If the syllable has a trailing consonant, return a tuple of three jamo characters
            if b:
                return (chr(q[0]), chr(q[1]), chr(q[2]))

            # Otherwise, return a tuple of two jamo characters
            return (chr(q[0]), chr(q[1]), '')

        # If the character is not a valid Korean syllable, return a tuple of empty strings and the character itself
        return ('', char, '')

    def _unpack(self, text: str) -> Generator[Tuple[str]]:
        """Unpacks a Korean text string into its constituent jamo characters.

        Parameters
        ----------
        text : str
            The input Korean text string to be unpacked into jamo.

        Yields
        ------
        Generator[Tuple[str]]
            A generator that yields tuples of jamo characters.
        """
        # Iterate over the indices of the characters in the input text
        for i in range(len(text)):
            # If the character is not the first or last one in the text
            if i not in [0, len(text)-1]:
                # Yield a tuple of jamo characters for the current character using the _jamo method
                yield self._jamo(text[i])
            # If the character is the first or last one in the text
            else:
                # If the character is the first one, yield a tuple of two or three jamo characters
                if i == 0:
                    yield ('', *self._jamo(text[i]))
                # If the character is the last one, yield a tuple of two or three jamo characters
                else:
                    yield (*self._jamo(text[i]), '', '')

    def read(self) -> str:
        """Reads input text and maps each chunk of three characters to a corresponding value 
        in a lookup table, returning the resulting text as a string.

        Returns
        -------
        str
            The output text.
        """
        # Call the stream method to generate the output text as a StringIO object
        output = self.stream()

        # Read the entire contents of the StringIO object as a string
        result = output.read()

        # Close the StringIO object to free up memory
        output.close()

        return result

    def stream(self) -> StringIO:
        """A generator function that reads input text and maps each chunk of three 
        characters to a corresponding value in a lookup table.

        Returns
        -------
        StringIO
            A file-like object containing the output text.
        """
        # If the input text has only one character, return it wrapped in a StringIO object
        if len(self.text) == 1:
            return StringIO(self.text)

        # Create an empty StringIO object to accumulate the output
        output = StringIO()

        # Loop over the chunks of three characters in the input text
        for chunk in self.chunks((j for i in self._unpack(self.text) for j in i), 3):
            # Corresponds value in the lookup table for the first two characters in the chunk
            try:
                output.write(self.__DATA[f"{chunk[0] or '-'}{chunk[1] or '-'}"])
            except KeyError:
                pass

            # Corresponds value in the lookup table for the third character in the chunk
            try:
                output.write(self.__DATA[f"-{chunk[2]}"])
            except KeyError:
                output.write(chunk[2])

        # Rewind the output StringIO object to the beginning and return it
        output.seek(0)

        return output

    @staticmethod
    def chunks(iterable: Iterable[Any], size: int) -> Iterator[List[str]]:
        """A generator function that yields lists of a given size from an iterable.

        Parameters
        ----------
        iterable : iterable
            The iterable to be split into chunks.
        size : int
            The maximum size of each chunk.

        Yields
        ------
        list
            A list of up to `size` items from the iterable.
        """
        # Define a lambda function to slice the generator `g` into chunks of size `size`
        def slice_size(g): return lambda: tuple(islice(g, size))

        # Return an iterator that applies the `slice_size` function to the input iterable
        return iter(slice_size(iter(iterable)), ())
