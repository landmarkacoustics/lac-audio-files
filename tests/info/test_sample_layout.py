# Copyright (C) 2021 by Landmark Acoustics LLC

import pytest

from lacaudiofiles.info.sample_layout import SampleLayoutInfo


@pytest.mark.parametrize('channels', [1, 2, 4, 8])
@pytest.mark.parametrize('interleaved', [True, False])
def test_sample_layout_info(channels, interleaved):
    r"""Do the layout attributes line up?"""

    layout = SampleLayoutInfo(channels, interleaved)

    assert layout.channels == channels
    assert layout.is_interleaved == interleaved

    dictionary = {
        'channels': channels,
        'interleaved': interleaved,
    }

    assert dict(layout) == dictionary
    assert str(layout) == str(dictionary)

    assert layout == SampleLayoutInfo(**dict(layout))
