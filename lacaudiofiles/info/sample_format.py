# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Basically a dumbed-down numpy.dtype."""

from .base_info import BaseInfo


class SampleFormatInfo(BaseInfo):
    r"""Cross-platform format information about a single piece of audio data.

    Parameters
    ----------
    size : int
        The number of bytes needed to store one sample.
    integer : bool
        If the data are stored as an integer (True) or a floating-point number.
    little_ended : bool
        If the  are stored as little- (True) or big- (False) ended.

    See Also
    --------
    numpy.dtype : A more sophisticated type that inspired this one.

    """

    key_names = [
        'size',
        'integer',
        'little_ended',
    ]

    val_names = [
        'byte_size',
        'is_integer',
        'is_little_ended',
    ]

    def __init__(self, size: int, integer: int, little_ended: bool):
        self._byte_size = size
        self._is_integer = integer
        self._is_little_ended = little_ended

    @property
    def byte_size(self) -> int:
        r"""How many bytes it takes to store one sample."""
        return self._byte_size

    @property
    def bit_size(self) -> int:
        r"""How many bits it takes to store one sample."""
        return self._byte_size * 8

    @property
    def is_integer(self) -> bool:
        r"""Is the sample an integer?"""
        return self._is_integer

    @property
    def is_floating_point(self) -> bool:
        r"""Is the sample a floating-point number?"""
        return not self._is_integer

    @property
    def is_little_ended(self) -> bool:
        r"""Is the sample stored in a little ended manner?"""
        return self._is_little_ended

    @property
    def is_big_ended(self) -> bool:
        r"""Is the sample stored in a big ended manner?"""
        return not self._is_little_ended

    @property
    def kind(self) -> str:
        r"""The numpy character code for integer or float."""
        return 'i' if self._is_integer else 'f'

    @property
    def byteorder(self) -> str:
        r"""The numpy character code for little- or big-ended."""
        return '<' if self._is_little_ended else '>'

    @property
    def dtype_code(self) -> str:
        r"""The numpy character code for the dtype for these samples."""
        return f'{self.byteorder}{self.kind}{self.byte_size}'
