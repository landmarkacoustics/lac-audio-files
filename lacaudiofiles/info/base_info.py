# Copyright (C) 2021 by Landmark Acoustics LLC
r"""Abstract base class for information objects."""


class BaseInfo:
    r"""Common behavior for Info-type objects in `lacaudiofiles`.

    Attributes
    ----------
    key_names : list[str]
        The arguments to the class constructor.
    val_names : list[str]
        The attributes where the class constructor's values are stored.

    """

    key_names = []
    val_names = []

    def __iter__(self) -> tuple:

        for k, v in zip(self.key_names, self.val_names):
            if callable(v):
                a = v(self)
            else:
                a = getattr(self, v)

            yield (k, a)

    def __repr__(self) -> str:
        return repr(dict(self))

    def __eq__(self, other) -> bool:
        return dict(self) == dict(other)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
