from collections.abc import Generator, Iterable, Iterator
from io import StringIO
from itertools import islice
from typing import Any, Dict, List, Tuple

import json
import os


class Hanguk:
    """A class to represent a Hanguk object.

    Attributes
    ----------
    text : str
        The text associated with the Hanguk object.

    Methods
    -------
    read()
        Returns the text associated with the Hanguk object.
    stream()
        Returns a StringIO object containing the text associated with the Hanguk object.
    """

    def __init__(self, text: str):
        """Constructs all the necessary attributes for the Hanguk object.

        Parameters
        ----------
            text : str
                The text associated with the Hanguk object.
        """
        self.text = text

    @property
    def _data(self) -> Dict:
        """Returns a dictionary containing data from a JSON file.

        Returns
        -------
            dict: A dictionary containing data from a JSON file.
        """
        with open(os.path.join(os.path.dirname(__file__), 'static', 'data.json'), 'r') as f:
            return json.load(f)

    def _jamo(self, char: str) -> Tuple[str]:
        """Returns a tuple of strings representing jamo characters for a given character.

        Parameters
        ----------
            char : str
                The character to be converted into jamo characters.

        Returns
        -------
            tuple: A tuple of strings representing jamo characters for a given character.
         """
        if 44032 <= (x := ord(char)) <= 55203:
            a = x - 44032
            b = a % 28
            c = 1 + ((a - b) % 588) // 28
            d = 1 + a // 588
            q = [*map(sum, zip(*[[d, c, b], [4351, 4448, 4519]]))]
            if b:
                return (chr(q[0]), chr(q[1]), chr(q[2]))
            return (chr(q[0]), chr(q[1]), '')
        return ('', char, '')

    def _unpack(self, text: str) -> Generator[Tuple[str]]:
        """Unpacks and returns jamo characters for each character in given text.

        Parameters:
        ----------
            text : str
                The string to be unpacked into jamo characters

        Returns:
        -------
            generator: A generator that yields tuples of strings representing jamo characters for each character in given text.
        """
        for i in range(len(text)):
            if i not in [0, len(text)-1]:
                yield self._jamo(text[i])
            else:
                if i == 0:
                    yield ('', *self._jamo(text[i]))
                else:
                    yield (*self._jamo(text[i]), '', '')

    def read(self) -> str:
        """Reads and returns the content of stream() method as string.

        Returns:
        -------
            str: The content of stream() method as string.
        """
        return self.stream().read()

    def stream(self) -> StringIO:
        """Streams and returns an instance of StringIO class containing processed output based on input `text`.

        Returns:
        --------
            StringIO: An instance of StringIO class containing processed output based on input `text`.
        """
        if len(self.text) == 1:
            return StringIO(self.text)
        output = StringIO()
        for chunk in self.chunks((j for i in self._unpack(self.text) for j in i), 3):
            try:
                output.write(self._data[f"{chunk[0] or '-'}{chunk[1] or '-'}"])
            except KeyError:
                pass
            try:
                output.write(self._data[f"-{chunk[2]}"])
            except KeyError:
                output.write(chunk[2])
        output.seek(0)
        return output

    @staticmethod
    def chunks(iterable: Iterable[Any], size: int) -> Iterator[List[str]]:
        """Returns an iterator that yields chunks from iterable of size `size`.

        Parameters :
        -------------
            iterable : Iterable[Any]
                An iterable to be chunked into smaller chunks.

            size : int
                Size of each chunk.

        Returns :
        --------
            iterator : An iterator that yields chunks from iterable of size `size`.
        """
        def slice_size(g): return lambda: tuple(islice(g, size))
        return iter(slice_size(iter(iterable)), ())
