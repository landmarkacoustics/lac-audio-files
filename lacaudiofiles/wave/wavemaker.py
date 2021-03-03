# Copyright (C) 2019 Landmark Acoustics LLC

r''' Landmark Acoustics' implementation of a wave audio writer.

    header format info cribbed from
    http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html

'''

import struct


class HeaderChunk:
    r'''Base for writing the start of any RIFF chunk.

    Parameters
    ----------
    id_code : str
        This identifies the type of chunk, based on a format definition.
    size : int
        The size, in bytes, of the rest of the chunk.

    '''

    def __init__(self,
                 id_code,
                 size):
        self._id_code = id_code
        self._size = size

    @classmethod
    def format(cls):
        r''' The format characters for packing the chunk's values.

        These are defined here:
        https://docs.python.org/3.6/library/struct.html#format-characters
        Subclasses should concatenate their format characters to the end
        of `super().format()`.

        '''

        return '4si'

    @property
    def size(self):
        r'''How long the chunk is, in bytes.'''
        return self._size

    def values(self):
        r''' The values that the chunk contains.

        These are (in part) defined here:
        http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html
        Subclasses should add a tuple of values to the end of
        `super().values()`.

        '''

        return (self._id_code.encode('ascii'),
                self._size)

    def as_bytes(self):
        r''' A `bytes` object that contains the chunk data.'''

        return struct.pack(self.format(),
                           *self.values())


class WaveChunk(HeaderChunk):
    r'''Writes the start of a WAVE chunk.

    Parameters
    ----------
    data_size : int
        The size, in bytes, of the file's sound data.

    '''

    def __init__(self,
                 data_size):
        super().__init__('RIFF',
                         4 + 24 + 8 + data_size)

    @classmethod
    def format(cls):
        return super().format() + '4s'

    def values(self):
        return super().values() + ('WAVE'.encode('ascii'),)


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


class DataChunk(HeaderChunk):
    r'''Writes the start of a chunk that describes a WAV file's data.

    Parameters
    ----------
    data_size : int
        The size, in bytes, of the file's sound data.

    '''

    def __init__(self,
                 data_size):
        super().__init__('data',
                         data_size)


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
    lacwebsockets.wavemaker.WaveChunk : the start of the header
    lacwebsockets.wavemaker.FormatChunk : the middle of the header
    lacwebsockets.wavemaker.DataChunk : the end of the header

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


if __name__ == '__main__':

    import numpy as np

    t = np.linspace(0, 0.1, 4410, endpoint=False)
    a = np.sin(2 * np.pi * 120 * t, dtype=np.float32)

    heads = {bits: WaveHeader(len(t), bits) for bits in [8, 16, 32]}

    amps = {
        8: np.array(2**7 * (1 + a), dtype=np.uint8),
        16: np.array(2**15 * a, dtype=np.int16),
        32: a,
    }

    for b, h in heads.items():

        with open(f'wave{b:02}.wav', 'wb') as fh:
            fh.write(h.as_bytes())
            fh.write(amps[b].tobytes())
