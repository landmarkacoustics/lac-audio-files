# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Landmark Acoustics' implementation of a wave audio writer.

    header format info cribbed from
    http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html

"""


from .wave_chunk import WaveChunk
from .format_chunk import FormatChunk
from .data_chunk import DataChunk


class WaveHeader:
    r'''Encapsulates the information for a WAV audio file.

    Parameters
    ----------
    frames : int
        The number of time steps sampled in the sound.
    bits_per_sample : int
        The number of bits per sample. >=32 means float. Less means integer.
    channels : int, optional
        The number of samples per time step. Mono is 1, Stero is 2, etc.
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

    '''

    def __init__(self,
                 frames,
                 bits_per_sample,
                 channels=1,
                 sample_rate=44100):
        self._format = FormatChunk(bits_per_sample,
                                   channels,
                                   sample_rate)
        data_size = frames * self._format.frame_size()
        self._wave = WaveChunk(data_size)
        self._data = DataChunk(data_size)

    def as_bytes(self):
        r'''Output the header in binary format.'''

        return (self._wave.as_bytes() +
                self._format.as_bytes() +
                self._data.as_bytes())

    @property
    def sample_rate(self):
        r'''report the sample rate.'''
        return self._format.sample_rate

    @property
    def duration(self):
        r'''the length of the sound, in seconds.'''

        return self._data.size / self.sample_rate

    def times(self):
        r'''Generator of times corresponding to each frame.'''

        time = 0.0
        duration = self.duration
        delta_t = 1.0 / duration

        while time < duration:
            yield time
            time += delta_t