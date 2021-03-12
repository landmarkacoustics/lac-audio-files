# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Landmark Acoustics' implementation of a wave audio writer.

    header format info cribbed from
    http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html

"""

import struct


from .wave_chunk import WaveChunk
from .format_chunk import FormatChunk
from .data_chunk import DataChunk


class WaveHeader:
    r"""Encapsulates the information for a WAV audio file.

    Parameters
    ----------
    frames : int
        The number of time steps sampled in the sound.
    bits_per_sample : int
        The number of bits per sample. >=32 means float. Less means integer.
    channels : int, optional
        The number of samples per time step. Mono is 1, Stereo is 2, etc.
    sample_rate : int, optional
        The number of frames measured per second.

    See Also
    --------
    lacaudiofiles.wave.WaveChunk : the start of the header
    lacaudiofiles.wave.FormatChunk : the middle of the header
    lacaudiofiles.wave.DataChunk : the end of the header

    Examples
    --------
    TBD

    """

    def __init__(self,
                 frames,
                 bits_per_sample,
                 channels=1,
                 sample_rate=44100):
        self._format = FormatChunk(bits_per_sample,
                                   channels,
                                   sample_rate)
        self._frames = frames
        data_size = frames * self._format.frame_size
        self._wave = WaveChunk(data_size)
        self._data = DataChunk(data_size)

    @classmethod
    def binary_format(cls) -> str:
        r"""The format that `struct` would use to pack or unpack this header.

        Returns
        -------
        str : a format string.

        """

        return ''.join([WaveChunk.format(),
                        FormatChunk.format(),
                        DataChunk.format()])

    @classmethod
    def unpack(cls, binary_data: bytes):
        r"""Create a WaveHeader from packed binary data.

        Parameters
        ----------
        binary_data : bytes
            A valid WAVE header in binary format.

        Returns
        -------
        WaveHeader : a new instance of this class.

        """

        (riff_string,
         file_size,
         wave_string,
         fmt__string,
         format_size,
         tag_code,
         channels,
         sample_rate,
         bytes_per_second,
         frame_size,
         bit_rate,
         data_string,
         data_size) = struct.unpack(cls.binary_format(),
                                    binary_data)

        assert riff_string == b'RIFF'
        assert wave_string == b'WAVE'
        assert fmt__string == b'fmt '
        assert data_string == b'data'

        header = cls(data_size // frame_size,
                     bit_rate,
                     channels,
                     sample_rate)

        assert header.as_bytes() == binary_data

        return header

    @property
    def sample_rate(self) -> int:
        r"""report the sample rate."""
        return self._format.sample_rate

    @property
    def frames(self) -> int:
        r"""report the number of samples"""
        return self._frames

    @property
    def duration(self) -> float:
        r"""the length of the sound, in seconds."""

        return self._data.size / self._format.frame_size / self.sample_rate

    def as_bytes(self) -> bytes:
        r"""Output the header in binary format."""

        return self._wave.as_bytes() + \
            self._format.as_bytes() + \
            self._data.as_bytes()

    def times(self) -> float:
        r"""Generator of times corresponding to each frame."""

        delta_t = 1.0 / self.sample_rate

        for f in range(self.frames):
            yield f * delta_t
