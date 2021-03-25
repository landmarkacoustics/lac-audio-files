# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Abstract base class for information objects."""

import inspect

class BaseInfo:
    r"""Common behavior for Info-type objects in `lacaudiofiles`.

    Subclasses should have a set of properties that have the exact same names
    as the arguments to their `__init__` functions.

    """

    def __iter__(self) -> tuple:

        for k in self.signature_keys():
            yield (k, getattr(self, k))

    def __repr__(self) -> str:
        return repr(dict(self))

    def __eq__(self, other) -> bool:
        return dict(self) == dict(other)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    @classmethod
    def signature_keys(cls) -> list:
        r"""Names of the inputs to this class. Also properties."""
        return list(inspect.signature(cls).parameters.keys())
