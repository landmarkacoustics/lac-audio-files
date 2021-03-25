# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Keeps track of basic info about digital sound data."""

from typing import (
    TypedDict,
    Union,
)

from .base import BaseInfo
from .sample import SampleInfo
from .frame import FrameInfo

from numpy import ndarray


class AudioInfo(BaseInfo):
    r"""You need at least this much information to store sounds digitally.

    Parameters
    ----------
    sample : Union[TypedDict, SampleInfo]
        Details about how individual values are stored.
    frame : Union[TypedDict, FrameInfo]
        Details about how the values are arranged into frames and channels. 
    sample_rate : int
        The number of samples per second in the data.

    See Also
    --------
    SampleInfo : information about, e.g., bit rate and endianness
    FrameInfo : the number of channels and if they're interleaved

    """

    def __init__(self,
                 sample: Union[TypedDict, SampleInfo],
                 frame: Union[TypedDict, FrameInfo], 
                 sample_rate: int) :

        self._format = _type_or_dict(sample,
                                     SampleInfo)

        self._layout = _type_or_dict(frame,
                                     FrameInfo)

        self._Hz = sample_rate

    @property
    def sample(self) -> SampleInfo:
        return self._format

    @property
    def frame(self) -> FrameInfo:
        return self._layout

    @property
    def sample_rate(self) -> int:
        return self._Hz

    @property
    def bits_per_second(self) -> float:
        return self._format.bit_size * self._layout.channels * self._Hz

    def numpy_array(self, data: bytes) -> ndarray:
        r"""Interpret the bytes in `data` as a numpy array.

        Parameters
        ----------
        data : bytes
            Binary data.

        Returns
        -------
        numpy.ndarray : a 2D array with dimensions of frames x channels.

        """

        samples = self.sample.length_in_samples(len(data))
        
        dim = (self.frame.frame_count(samples),
               self.frame.channels)

        order = ['C', 'F'][self.frame.is_interleaved]

        return ndarray(dim,
                       dtype=self.sample.dtype_code,
                       order=order,
                       buffer=data)

def _type_or_dict(obj, cls):
    if type(obj) == cls:
        return obj
    else:
        return cls(**obj)
