# Copyright (C) 2021 by Landmark Acoustics LLC
r"""helpful functions for dealing with information objects"""


def type_or_dict(obj, cls):
    if type(obj) == type(cls):
        return obj
    else:
        return cls(**obj)
