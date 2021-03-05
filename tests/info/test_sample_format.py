# Copyright (C) 2021 by Landmark Acoustics LLC

from sys import byteorder as system_byteorder

from numpy import dtype

import pytest

from lacaudiofiles.info.sample_format import SampleFormatInfo


@pytest.mark.parametrize('size', [1, 2, 4, 8])
@pytest.mark.parametrize('kind', ['float', 'integer'])
@pytest.mark.parametrize('order', ['little', 'big'])
def test_sample_format_info(size, kind, order):
    r"""Do the format attributes line up?"""

    if kind == 'float' and size < 2:
        pytest.skip()

    is_integer = kind == 'integer'
    is_little_ended = order == 'little'

    byteorder = ['>', '<'][is_little_ended]
    code = f'{byteorder}{kind[0]}{size}'

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

    dictionary = {
        'size': size,
        'integer': is_integer,
        'little_ended' : is_little_ended,
    }

    assert dict(info) == dictionary

    assert str(info) == str(dictionary)
