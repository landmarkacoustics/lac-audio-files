# Copyright (C) 2021 by Landmark Acoustics LLC

import pytest

from lacaudiofiles.wave.wave_chunk import WaveChunk

from helpers import chunk_bytes


def test_static_methods():
    r"""The format should always be the same."""
    assert WaveChunk.format() == r'4si4s'


@pytest.mark.parametrize('size', [2**x for x in range(12)])
def test_wave_chunk(size):

    chunk = WaveChunk(size)
    size += 36
    assert chunk.code == r'RIFF'
    assert chunk.size == size
    assert chunk.values() == (b'RIFF', size, b'WAVE')
    assert chunk.as_bytes() == chunk_bytes('RIFF', size) + b'WAVE'
