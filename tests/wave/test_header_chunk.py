# Copyright (C) 2021 by Landmark Acoustics LLC

import struct

import pytest

from lacaudiofiles.wave.header_chunk import HeaderChunk

def test_format_code():
    r"""This is a constant."""
    assert HeaderChunk.format() == '4si'


@pytest.fixture
def code_size_answer(request):
    code, size = request.param
    answer = struct.pack('4si',
                         code.encode('ascii'),
                         size)
    return (
        code,
        size,
        answer
    )

@pytest.mark.parametrize('code_size_answer', [
    ('fooo', 42),
    ('barr', 1),
    ('----', 99),
    ('fail', -1)
],
                         indirect=True)
def test_header_chunk(code_size_answer):
    code, size, answer = code_size_answer
    head = HeaderChunk(code, size)
    assert head.size == size
    assert head.values() == (
        code.encode('ascii'),
        size)
    assert head.as_bytes() == answer


def bad_codes_fail():
    with pytest.raises(ValueError) as info:
        head = HeaderChunk('foo', 2)

    assert info.value.value == 'the code must be four characters long.'
