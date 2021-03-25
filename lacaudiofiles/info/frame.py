# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Keeps track of how samples are arranged into an audio file."""

from .base import BaseInfo


class FrameInfo(BaseInfo):
    r"""The way that individual samples are arranged in a sound file.

    Parameters
    ----------
    channels : int, optional
        The number of channels in the data. The default is one.
    is_interleaved : bool, optional
        `True` (the default) when the data are grouped by time, not by channel.

    Attributes
    ----------
    Each of the parameters is stored as a property.

    """

    def __init__(self,
                 channels: int=1,
                 is_interleaved: bool=True) :

        self._channels = channels
        self._interleaved = is_interleaved

    @property
    def channels(self) -> int:
        return self._channels

    @property
    def is_interleaved(self) -> bool:
        return self._interleaved

    def frame_count(self, sample_count: int) -> int:
        r"""The number of frames in a piece of data with `sample_count` items.

        Parameters
        ----------
        sample_count : int
            The number of samples, not necessarily bytes, in some binary data.

        Returns
        -------
        int : the number of frames in some binary data

        """

        return sample_count // self.channels
