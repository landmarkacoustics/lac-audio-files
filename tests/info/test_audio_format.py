# Copyright (C) 2021 by Landmark Acoustics LLC

from sys import byteorder as system_byteorder

import numpy as np

from numpy.testing import assert_allclose, assert_array_equal

import pytest

from lacaudiofiles.info.sample_format import SampleFormatInfo
from lacaudiofiles.info.sample_layout import SampleLayoutInfo
from lacaudiofiles.info.audio_format import AudioFormatInfo

@pytest.fixture(scope='module',
                params=[
                    (2, 'integer'),
                    (4, 'integer'),
                    (8, 'integer'),
                    (4, 'float'),
                    (8, 'float'),
                ])
def data_type(request):
    r"""A 2-tuple of byte-size and floating-point"""
    return request.param


@pytest.fixture(scope='module',
                params=['little', 'big'])
def order(request):
    r"""Text that describes the endianness of the data."""
    return request.param


@pytest.fixture(scope='module')
def format_info(data_type,
                order):
    r"""A SampleFormatInfo object"""
    size, kind = data_type
    return SampleFormatInfo(size,
                            kind=='integer',
                            order=='little')


@pytest.fixture(scope='module',
                params=[1, 44100, 98000])
def Hz(request):
    r"""The sample rate of the sound."""
    return request.param


@pytest.fixture(scope='module',
                params=[1, 2, 4])
def channels(request):
    r"""The number of channels in the sound data."""
    return request.param


@pytest.fixture(scope='module',
                         params=[True, False])
def is_interleaved(request):
    r"""Whether the data are organized by channel rather than frame."""
    return request.param


@pytest.fixture(scope='module')
def layout_info(channels,
                is_interleaved):
    r"""A SampleLayoutInfo object."""
    return SampleLayoutInfo(channels,
                            is_interleaved)


def test_audio_format_info(format_info,
                           layout_info,
                           Hz):

    info = AudioFormatInfo(format_info,
                           layout_info,
                           Hz)

    bps = format_info.bit_size * layout_info.channels * Hz

    assert info.sample_rate == Hz

    audio_dict = {
        'sample_format' : dict(format_info),
        'sample_layout' : dict(layout_info),
        'sample_rate' : Hz,
    }

    assert dict(info) == audio_dict

    assert str(info) == str(audio_dict)

    assert info == AudioFormatInfo(**dict(info))

    x = np.arange(10, dtype=format_info.dtype_code).reshape(10, 1)

    X = np.tile(x, (1, layout_info.channels))

    if layout_info.is_interleaved:
        byte_data = layout_info.channels * x.tobytes()
    else:
        byte_data = X.tobytes()

    if format_info.is_integer:
        compare = assert_array_equal
    else:
        compare = assert_allclose

    compare(info.numpy_array(byte_data), X)
