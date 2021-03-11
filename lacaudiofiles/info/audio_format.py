# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Keeps track of basic info about digital sound data."""

from typing import (
    TypedDict,
    Union,
)

from .base_info import BaseInfo
from .sample_format import SampleFormatInfo
from .sample_layout import SampleLayoutInfo

class AudioFormatInfo(BaseInfo):
    r"""You need at least this much information to store sounds digitally.

    Parameters
    ----------
    sample_format : Union[TypedDict, SampleFormatInfo]
        Details about how individual values are stored.
    sample_layout : Union[TypedDict, SampleLayoutInfo]
        Details about how the values are arranged into frames and channels. 
    sample_rate : int
        The number of samples per second in the data.

    See Also
    --------
    SampleFormatInfo : information about, e.g., bit rate and endianness
    SampleLayoutInfo : the number of channels and if they're interleaved
    """

    key_names = [
        'sample_format',
        'sample_layout',
        'sample_rate',
    ]

    val_names = [
        lambda x: dict(x.sample_format),
        lambda x: dict(x.sample_layout),
        'sample_rate',
    ]

    def __init__(self,
                 sample_format: Union[TypedDict, SampleFormatInfo],
                 sample_layout: Union[TypedDict, SampleFormatInfo], 
                 sample_rate: int) :

        self._format = _type_or_dict(sample_format,
                                     SampleFormatInfo)

        self._layout = _type_or_dict(sample_layout,
                                     SampleLayoutInfo)

        self._Hz = sample_rate

    @property
    def sample_format(self) -> SampleFormatInfo:
        return self._format

    @property
    def sample_layout(self) -> SampleLayoutInfo:
        return self._layout

    @property
    def sample_rate(self) -> int:
        return self._Hz

    @property
    def bits_per_second(self) -> float:
        return self._format.bit_size * self._layout.channels * self._Hz


def _type_or_dict(obj, cls):
    if type(obj) == cls:
        return obj
    else:
        return cls(**obj)
