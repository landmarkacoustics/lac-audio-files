# Copyright (C) 2021 by Landmark Acoustics LLC

import pytest

from lacaudiofiles.info.base_info import BaseInfo


def test_naked_base_info():
    r"""Everything should just be blank."""

    bi = BaseInfo()

    assert dict(bi) == {}
    assert repr(bi) == '{}'

    assert bi == BaseInfo()

    assert bi == BaseInfo(**dict(bi))


class Modified(BaseInfo):

    def __init__(self, foo, bar, baz):
        self._foo = foo
        self._bar = bar
        self._baz = baz

    @property
    def foo(self):
        return self._foo

    @property
    def bar(self):
        return self._bar

    @property
    def baz(self):
        return self._baz


def test_modified_base_info():
    r"""Add some values to the keys and values and check functionality."""

    castor = Modified(3, 1, 4)
    pollux = Modified(**dict(castor))
    cadmus = Modified(7, 7, 7)

    assert castor == pollux
    assert castor != cadmus
    assert pollux != cadmus

    dictionary = {
        'foo': 3,
        'bar': 1,
        'baz': 4,
    }

    assert dict(castor) == dictionary
    assert str(pollux) == str(dictionary)

    for k in dictionary:
        dictionary[k] = 7

    assert dict(cadmus) == dictionary
    assert str(cadmus) == str(dictionary)
