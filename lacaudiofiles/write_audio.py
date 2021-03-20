# Copyright (C) 2021 by Landmark Acoustics LLC

from typing import BinaryIO

import numpy as np

from .info import AudioFormatInfo


def write_audio(source_array: np.ndarray,
                format_info: AudioFormatInfo,
                target_stream: BinaryIO) -> int:
    r"""Write the data to a stream in the specific format.

    Parameters
    ----------
    source_array : numpy.ndarray
        A frames by channels array of audio data
    format_info : AudioFormatInfo
        The format that the output should be in
    target_stream : BinaryIO
        The stream to write the data to

    Returns
    -------
    int : the number of bytes written

    """

    if format_info.sample_layout.is_interleaved:
        source_array = source_array.T
    
    buffer = np.zeros(source_array.shape[1],
                      dtype=format_info.sample_format.dtype_code)

    n = 0

    for x in source_array:
        buffer[:] = x
        n += target_stream.write(buffer.tobytes())

    return n

            
