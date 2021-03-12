# Copyright (C) 2021 by Landmark Acoustics LLC

from struct import pack

import pytest

from lacaudiofiles.wave.wave_header import WaveHeader

from helpers import chunk_bytes


def test_wave_header_binary_format():
    r"""Does this static method produce what it should?"""

    should_be = '4si4s' + '4siHhiihh' + '4si'

    assert WaveHeader.binary_format() == should_be


@pytest.mark.parametrize('data,answer', [
    (b'RIFF\xe08\x07\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\xbc8\x07\x00',
     {
         'integer': True,
         'sample_rate': 44100,
         'bit_rate': 16,
         'channels': 1,
         'frames': 236638,
     }),
    (b'RIFF\xacX\x01\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x88X\x01\x00',
     {
         'integer': True,
         'sample_rate': 44100,
         'bit_rate': 16,
         'channels': 1,
         'frames': 44100,
     }),
    (b'RIFFDb\x05\x00WAVEfmt \x10\x00\x00\x00\x03\x00\x02\x00D\xac\x00\x00 b\x05\x00\x08\x00 \x00data b\x05\x00',
     {
         'integer': False,
         'sample_rate': 44100,
         'bit_rate': 32,
         'channels': 2,
         'frames': 44100,
     }),
],
                          ids=['chirp', 'mono', 'tones'])
def test_unpack_binary_to_wave_header(data, answer):
    r"""unpack binary header data and create the header object."""
    header = WaveHeader.unpack(data)

    assert header.sample_rate == answer['sample_rate']
    assert header.frames == answer['frames']
    assert header.duration == answer['frames'] / answer['sample_rate']

    assert header._format.frame_size == answer['bit_rate'] * answer['channels'] // 8
    assert header._format._tag == 1 if answer['integer'] else 3


@pytest.fixture(scope='module',
                params=[-1, 0, 1, 99000])
def frames(request):
    r"""The number of frames in the wave file."""
    return request.param


@pytest.fixture(scope='module',
                params=[8, 32, 64])
def bits(request):
    r"""The number of bits per sample in the wave file."""
    return request.param


@pytest.fixture(scope='module',
                params=[1, 2, 4])
def channels(request):
    r"""The number of channels in the wave file."""
    return request.param


@pytest.fixture(scope='module',
                params=[1, 44100, 98000])
def Hz(request):
    r"""The sample rate of the wave file."""
    return request.param


def test_wave_header_starts(frames, bits, channels, Hz):
    r"""Does the wave header assemble itself correctly?"""

    wh = WaveHeader(frames,
                    bits,
                    channels,
                    Hz)

    assert wh.sample_rate == Hz
    assert wh.duration == frames / Hz


def test_wave_header_as_bytes(frames, bits, channels, Hz):
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


def test_wave_header_times(frames, bits, channels, Hz):
    r"""Generate times for each frame of the file."""

    wh = WaveHeader(frames, bits, channels, Hz)

    assert wh.duration == frames / Hz

    expected_times = [x/Hz for x in range(frames)]
    observed_times = [x for x in wh.times()]

    assert observed_times == pytest.approx(expected_times)
