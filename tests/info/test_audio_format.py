# Copyright (C) 2021 by Landmark Acoustics LLC

# Copyright (C) 2021 by Landmark Acoustics LLC

from sys import byteorder as system_byteorder

import numpy as np

from numpy.testing import assert_allclose, assert_array_equal

import pytest

from lacaudiofiles.info.sample_format import SampleFormatInfo
from lacaudiofiles.info.sample_layout import SampleLayoutInfo
from lacaudiofiles.info.audio_format import AudioFormatInfo

@pytest.mark.parametrize('data_type', [
    (2, 'integer'),
    (4, 'integer'),
    (8, 'integer'),
    (4, 'float'),
    (8, 'float'),
])
@pytest.mark.parametrize('order', ['little', 'big'])
@pytest.mark.parametrize('Hz', [1, 44100, 98000])
@pytest.mark.parametrize('channels', [1, 2, 4])
@pytest.mark.parametrize('interleaved', [True, False])
def test_audio_format_info(data_type, order, Hz, channels, interleaved):

    size, kind = data_type

    is_integer = kind == 'integer'
    is_little_ended = order == 'little'

    format_info = SampleFormatInfo(size,
                                   is_integer,
                                   is_little_ended)

    layout_info = SampleLayoutInfo(channels,
                                   interleaved)

    info = AudioFormatInfo(format_info,
                           layout_info,
                           Hz)

    assert info.bits_per_second == size * 8 * channels * Hz

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

    X = np.tile(x, (1, channels))

    byte_data = channels * x.tobytes() if interleaved else X.tobytes()

    compare = assert_array_equal if is_integer else assert_allclose

    compare(info.numpy_array(byte_data), X)
