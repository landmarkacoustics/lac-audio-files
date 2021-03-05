# Copyright (C) 2021 by Landmark Acoustics LLC

from sys import byteorder as system_byteorder

from numpy import dtype

import pytest

from lacaudiofiles.sample_format_info import SampleFormatInfo


@pytest.mark.parametrize('size,kind,order,code', [
    (4, 'float', 'little', '<f4'),
    (8, 'float', 'little', '<f8'),
    (4, 'float', 'big', '>f4'),
    (8, 'float', 'big', '>f8'),
    (1, 'integer', 'little', '<i1'),
    (2, 'integer', 'little', '<i2'),
    (4, 'integer', 'little', '<i4'),
    (8, 'integer', 'little', '<i8'),
    (1, 'integer', 'big', '>i1'),
    (2, 'integer', 'big', '>i2'),
    (4, 'integer', 'big', '>i4'),
    (8, 'integer', 'big', '>i8'),
])
def test_sample_format_info(size, kind, order, code):
    r"""Do the attributes line up?"""

    is_integer = kind == 'integer'
    is_little_ended = order == 'little'

    byteorder = ['>', '<'][is_little_ended]
    
    info = SampleFormatInfo(size,
                            is_integer,
                            is_little_ended)

    assert info.byte_size == size

    assert info.bit_size == 8*size

    assert info.is_integer == is_integer

    assert not info.is_floating_point == is_integer

    assert info.is_little_ended == is_little_ended

    assert not info.is_big_ended == is_little_ended

    assert info.kind == kind[0]

    assert info.byteorder == byteorder

    assert info.dtype_code == code

    result = dtype(info.dtype_code)

    if system_byteorder == order:
        byteorder = '='

    if size == 1:
        byteorder = '|'

    assert result.byteorder == byteorder
    assert result.kind == kind[0]
    assert result.itemsize == size
