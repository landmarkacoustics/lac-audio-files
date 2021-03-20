# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Convert a stream of data into a new audio codec."""

from typing import BinaryIO
from . import AudioFormatInfo


class Converter:
    r"""Convert audio formats between streams.

    Parameters
    ----------
    out_stream : BinaryIO
        A seekable file-like stream for audio output
    out_format : AudioFormatInfo
        The format of the output stream
    buffer_size : int, optional
        How big of a buffer the converter should use. Defaults to 1MB.

    """

    def __init__(self,
                 out_stream : BinaryIO,
                 out_format : AudioFormatInfo,
                 buffer_size : int=None) :

        self._stream = out_stream
        self._format = out_format
        if buffer_size is None:
            buffer_size = 1024 * 1024 // self._format.sample_format.byte_size

        self._buffer = bytes(buffer_size)

    def convert(self,
                 in_stream : BinaryIO,
                 in_format : AudioFormatInfo):
        r"""Carry out the conversion.

        Parameters
        ----------
        in_stream : BinaryIO
            A read-only stream of raw audio input.
        in_format : AudioFormatInfo
            The format of the input stream

        Returns
        -------
        bool : success or failure
 
        """

        a = np.array(in_stream.read(),
                     dtype = in_format.dtype_code())

        for x in nditer(a, op_dtypes=[self._format.dtype_code()]):
            self._stream.write()
        while not in_stream.eof:
            n_read = in_stream.read_to(self._buffer, len(self._buffer))
            if n_read:
                self.convert_buffer()
                self._stream.write(self._buffer)
                self._stream.flush()

