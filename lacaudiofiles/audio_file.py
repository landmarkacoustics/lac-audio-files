# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Read/write access to audio data."""

from typing import BinaryIO
from . import AudioFormatInfo


class AudioFile:
    r"""Right now I'm just sketching this.

    Parameters
    ----------
    stream : BinaryIO
        The file or socket where the data originates from or goes to.
    format_info : AudioFormatInfo
        The details about how the bytes are arranged, not the codec.
    codec : str
        I actually anticipate using mixins for this.

    """

    def __init__(self,
                 stream: BinaryIO,
                 format_info: AudioFormatInfo,
                 codec: str):
        self._stream = stream
        self._format = format_info
        self._is_readable = stream.readable()
        self._is_writeable = stream.writeable()

    
