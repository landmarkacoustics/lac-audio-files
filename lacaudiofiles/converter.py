# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Convert a stream of data into a new audio codec."""

from typing import BinaryIO
from . import AudioFormatInfo


class Converter:
    r"""Convert audio formats between streams.

    Parameters
    ----------
    in_stream : BinaryIO
        A read-only stream of raw audio input.
    out_stream : BinaryIO
        A seekable file-like stream for audio output
    """
