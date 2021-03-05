# Copyright (C) 2019 Landmark Acoustics LLC

import struct








if __name__ == '__main__':

    import numpy as np

    t = np.linspace(0, 0.1, 4410, endpoint=False)
    a = np.sin(2 * np.pi * 120 * t, dtype=np.float32)

    heads = {bits: WaveHeader(len(t), bits) for bits in [8, 16, 32]}

    amps = {
        8: np.array(2**7 * (1 + a), dtype=np.uint8),
        16: np.array(2**15 * a, dtype=np.int16),
        32: a,
    }

    for b, h in heads.items():

        with open(f'wave{b:02}.wav', 'wb') as fh:
            fh.write(h.as_bytes())
            fh.write(amps[b].tobytes())
