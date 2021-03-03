# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Helper functions and classes for testing the `wave` subpackage."""

import struct


def chunk_bytes(code, size) -> bytes:
    r"""Pack the code and size into a bytes object."""
    return struct.pack('4si',
                       code.encode('ascii'),
                       size)
