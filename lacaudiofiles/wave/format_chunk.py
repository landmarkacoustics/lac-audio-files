# Copyright (C) 2021 by Landmark Acoustics LLC

from .header_chunk import HeaderChunk


class FormatChunk(HeaderChunk):
    r'''Writes the entire chunk that describes a WAV file's format.

    Parameters
    ----------
    bit_rate : int
        The size of one sound measurement for one channel.

        This is also used to determine the PCM format of the data. Any bit rate
        smaller than 32 will be encoded as an integer (tag `0x0001`), while
        larger bit rates will be encoded as floating-point (tag `0x0003`).

    channels : int
        The number of channels that the sound has (1 for mono, 2 for stereo).

    sample_rate : int
        The number of frames per second, where a frame has `channels` samples.

    '''

    def __init__(self,
                 bit_rate,
                 channels,
                 sample_rate):
        super().__init__('fmt ', 16)
        self._tag = 0x0003 if bit_rate >= 32 else 0x0001
        self._channels = channels
        self._sample_rate = sample_rate
        self._frame_size = channels * (bit_rate // 8)
        self._bytes_per_sec = self._frame_size * sample_rate
        self._bit_rate = bit_rate

    @property
    def frame_size(self):
        r'''The number of bytes in one instanc of samples from each channel'''
        return self._frame_size

    @property
    def sample_rate(self):
        r'''The number of frames per second'''
        return self._sample_rate

    @classmethod
    def format(cls):
        return super().format() + 'Hhiihh'

    def values(self):
        return super().values() + (
            self._tag,
            self._channels,
            self._sample_rate,
            self._frame_size * self._sample_rate,
            self._frame_size,
            self._bit_rate,
        )