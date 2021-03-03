# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Test the kind of chunk that tracks WAV format information."""

import pytest

from lacaudiofiles.wave.format_chunk import FormatChunk

def test_static_functions():
    r"""The `format` method is static."""
    assert FormatChunk.format() == r'4siHhiihh'


def test_constant_chunk_size():
    r"""The format chunk should always be 16 bytes long."""
    unrealisitic_chunk = FormatChunk(10, 20, 30)
    assert unrealisitic_chunk.size == 16

    realistic_chunk = FormatChunk(16, 2, 44100)
    assert realistic_chunk.size == 16


@pytest.mark.parametrize('bit_rate', range(1, 8))
def test_tiny_samples_fail(bit_rate):
    r"""A sample must have at least one byte."""
    with pytest.raises(ValueError) as info:
        chunk = FormatChunk(bit_rate, 10, 100)



@pytest.mark.parametrize('sample_rate', [1, 1000, 44100, 98000])
@pytest.mark.parametrize('channels', [1, 2, 4])
@pytest.mark.parametrize('bit_rate', [2**x for x in range(3, 10)])
def test_format_chunk_properties(sample_rate,
                                 channels,
                                 bit_rate):
    r"""Check the properties established by the ctor."""

    chunk = FormatChunk(bit_rate,
                        channels,
                        sample_rate)

    assert chunk.code == 'fmt '
    assert chunk.size == 16

    frame_size = channels * (bit_rate // 8)
    assert chunk.frame_size == frame_size
    assert chunk.sample_rate == sample_rate

    assert chunk.values() == (
        b'fmt ',
        16,
        0x003 if bit_rate >= 32 else 0x001,
        channels,
        sample_rate,
        frame_size * sample_rate,
        frame_size,
        bit_rate
    )
