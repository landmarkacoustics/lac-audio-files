# Copyright (C) 2021 by Landmark Acoustics LLC

from io import BytesIO

import numpy as np

from numpy.testing import assert_allclose

import pytest

from lacaudiofiles.info import (
    AudioInfo,
    SampleInfo,
    FrameInfo,
)

from lacaudiofiles.write_audio import write_audio


@pytest.fixture(scope='module',
                params=[True, False])
def is_le(request):
    r"""Whether the binary data stored as little-endian."""
    return request.param


@pytest.fixture(scope='module',
                params=[
                    (1, True),
                    (2, True),
                    (4, True),
                    (4, False),
                    (8, True),
                    (8, False),
                ])
def type_and_size(request):
    r"""Integer or floating-point and bytes per item in a 2-tuple"""
    return request.param


@pytest.fixture(scope='module')
def fmt(type_and_size, is_le) -> SampleInfo:
    r"""A SampleInfo object."""
    bytesize, is_integer = type_and_size
    return SampleInfo(bytesize,
                      is_integer,
                      is_le)


@pytest.fixture(scope='module',
                params=[True, False])
def is_interleaved(request):
    r"""Whether the data are arranged as channels"""
    return request.param


@pytest.fixture(scope='module')
def initial_data(request) -> np.ndarray:
    r"""some fake data."""

    x = np.arange(4)
    return np.c_[x, -7 - x]


def test_writing_different_ends(fmt,
                                is_interleaved,
                                initial_data):
    r"""I don't know if the endianness works"""

    layout = FrameInfo(initial_data.shape[1],
                       is_interleaved)

    info = AudioInfo(fmt, layout, 44100)

    stream = BytesIO(b'0' * initial_data.size)

    bytes_written = write_audio(initial_data,
                                info,
                                stream)

    assert bytes_written == initial_data.size * fmt.byte_size

    output_data = info.numpy_array(stream.getbuffer())

    assert_allclose(initial_data, output_data)

    if layout.is_interleaved:
        assert bytes(stream.getbuffer()) != output_data.tobytes()
    else:
        assert bytes(stream.getbuffer()) == output_data.tobytes()
