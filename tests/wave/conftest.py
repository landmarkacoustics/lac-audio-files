# Copyright (C) 2021 by Landmark Acoustics LLC

import pytest

from helpers import chunk_bytes


@pytest.fixture
def code_size_answer(request):
    code, size = request.param
    answer = chunk_bytes(code, size)
    return (
        code,
        size,
        answer
    )
