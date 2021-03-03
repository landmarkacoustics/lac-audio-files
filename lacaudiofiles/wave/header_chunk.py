# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Base class for the chunks that go in headers."""

import struct


class HeaderChunk:
    r"""Base for writing the start of any RIFF chunk.

    Parameters
    ----------
    id_code : str
        This identifies the type of chunk, based on a format definition.
    size : int
        The size, in bytes, of the rest of the chunk.

    """

    def __init__(self,
                 id_code,
                 size):
        if len(id_code) != 4:
            raise ValueError('the code must be four characters long.')

        self._id_code = id_code
        self._size = size

    @classmethod
    def format(cls):
        r""" The format characters for packing the chunk's values.

        These are defined here:
        https://docs.python.org/3.6/library/struct.html#format-characters
        Subclasses should concatenate their format characters to the end
        of `super().format()`.

        """

        return '4si'

    @property
    def code(self) -> str:
        r"""The chunk's ID code."""
        return self._id_code

    @property
    def size(self) -> int:
        r"""How long the chunk is, in bytes."""
        return self._size

    def values(self) -> struct:
        r""" The values that the chunk contains.

        These are (in part) defined here:
        http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html
        Subclasses should add a tuple of values to the end of
        `super().values()`.

        """

        return (self._id_code.encode('ascii'),
                self._size)

    def as_bytes(self) -> bytes:
        r""" A `bytes` object that contains the chunk data."""

        return struct.pack(self.format(),
                           *self.values())
