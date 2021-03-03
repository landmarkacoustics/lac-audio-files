# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Not the actual data, but the chunk that says how big the data are."""

from .header_chunk import HeaderChunk


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
