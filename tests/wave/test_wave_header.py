# Copyright (C) 2021 by Landmark Acoustics LLC

from struct import pack

import pytest

from lacaudiofiles.wave.wave_header import WaveHeader

from helpers import chunk_bytes


@pytest.mark.parametrize('frames', [1, 10, 20, 42, 99000])
@pytest.mark.parametrize('bits', [2**x for x in range(3, 10)])
@pytest.mark.parametrize('channels', [1, 2, 4])
@pytest.mark.parametrize('Hz', [1, 1000, 44100, 98000])
def test_wave_header_starts(frames,
                            bits,
                            channels,
                            Hz):
    r"""Does the wave header assemble itself correctly?"""

    wh = WaveHeader(frames,
                    bits,
                    channels,
                    Hz)

    assert wh.sample_rate == Hz
    assert wh.duration == frames / Hz


@pytest.mark.parametrize('frames', [1, 10, 20, 42, 99000])
@pytest.mark.parametrize('bits', [2**x for x in range(3, 10)])
@pytest.mark.parametrize('channels', [1, 2, 4])
@pytest.mark.parametrize('Hz', [1, 1000, 44100, 98000])
def test_wave_header_as_bytes(frames,
                              bits,
                              channels,
                              Hz):
    r"""The bytes representation of a WaveHeader is actually quite long."""

    wh = WaveHeader(frames, bits, channels, Hz)

    frame_size = channels * (bits // 8)
    data_size = frames * frame_size
    chunk_length = 4 + 24 + 8 + data_size

    wave_chunk = chunk_bytes('RIFF', chunk_length) + b'WAVE'

    format_chunk = chunk_bytes('fmt ', 16) + \
        pack('Hhiihh',
             0x001 if bits < 32 else 0x003,
             channels,
             Hz,
             frame_size * Hz,
             frame_size,
             bits)

    data_chunk = chunk_bytes('data', data_size)

    assert wh.as_bytes() == wave_chunk + format_chunk + data_chunk


@pytest.mark.parametrize('frames', [1, 10, 20, 42, 99000])
@pytest.mark.parametrize('bits', [2**x for x in range(3, 10)])
@pytest.mark.parametrize('channels', [1, 2, 4])
@pytest.mark.parametrize('Hz', [1, 1000, 44100, 98000])
def test_wave_header_times(frames,
                           bits,
                           channels,
                           Hz):
    r"""Generate times for each frame of the file."""

    wh = WaveHeader(frames, bits, channels, Hz)

    assert wh.duration == frames / Hz

    expected_times = [x/Hz for x in range(frames)]
    observed_times = [x for x in wh.times()]

    assert observed_times == pytest.approx(expected_times)
