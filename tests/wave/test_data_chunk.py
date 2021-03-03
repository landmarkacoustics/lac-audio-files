# Copyright (C) 2021 by Landmark Acoustics LLC

import pytest

from lacaudiofiles.wave.data_chunk import DataChunk

from helpers import chunk_bytes


@pytest.mark.parametrize('size', [42, -1, 33, 99])
def test_data_chunk(size):
    r"""The data chunk's size can change but its id should always be 'data'"""

    chunk = DataChunk(size)

    assert chunk.code == 'data'
    assert chunk.size == size
    assert chunk.values() == (b'data', size)
    assert chunk.as_bytes() == chunk_bytes('data', size)
