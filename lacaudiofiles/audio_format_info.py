# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Keeps track of basic info about digital sound data."""

import struct


class AudioFormatInfo:
    r"""You need at least this much information to store sounds digitally.

    Parameters
    ----------
    sample_rate : int
        The number of samples per second in the data.
    element_format : str
        The format code from the `struct` module that describes the data.
    channels : int, optional
        The number of channels in the data. The default is one.
    interleaved : bool, optional
        `True` (the default) when the data are grouped by time, not by channel.

    Attributes
    ----------
    Each of the parameters is stored as a property.

    See Also
    --------
    json : for serializing
    struct : for the format codes

    """

    def __init__(self,
                 sample_rate: int,
                 element_format: str,
                 channels: int=1,
                 interleaved: bool=True) :

        self._Hz = sample_rate
        self._format = element_format
        self._channels = channels
        self._interleaved = interleaved

    @property
    def sample_rate(self) -> int:
        return self._Hz

    @property
    def element_format(self) -> str:
        return self._format

    @property
    def channels(self) -> int:
        return self._channels

    @property
    def interleaved(self) -> bool:
        return self._interleaved

    def as_dict(self) -> dict:
        return {
            'sample_rate': self.sample_rate,
            'element_format': self.element_format,
            'channels': self.channels,
            'interleaved': self.interleaved
        }

    def __repr__(self) -> str:
        return repr(self.as_dict())
