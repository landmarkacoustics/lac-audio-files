# Copyright (C) 2021 by Landmark Acoustics LLC

import pytest

from lacaudiofiles.info import FrameInfo


@pytest.mark.parametrize('channels', [1, 2, 4, 8])
@pytest.mark.parametrize('interleaved', [True, False])
def test_frame_info(channels, interleaved):
    r"""Do the frame attributes line up?"""

    layout = FrameInfo(channels, interleaved)

    assert layout.channels == channels
    assert layout.is_interleaved == interleaved

    dictionary = {
        'channels': channels,
        'is_interleaved': interleaved,
    }

    assert dict(layout) == dictionary
    assert str(layout) == str(dictionary)

    assert layout == FrameInfo(**dict(layout))

    sample_count = 42

    assert sample_count // layout.channels == layout.frame_count(sample_count)
