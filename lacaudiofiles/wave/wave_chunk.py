# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Not the data but a chunk that identifies the file type as WAVE."""

from .header_chunk import HeaderChunk


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
