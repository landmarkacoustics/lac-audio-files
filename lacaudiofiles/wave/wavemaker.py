# Copyright (C) 2019 Landmark Acoustics LLC

import struct

import numpy as np

phi = 100
Hz = 44100
taus = 2 * np.pi * np.linspace(0, 1, Hz, False)

# mono 16-bit integer
atype = np.dtype('<h')
a = np.array(np.sin(phi * taus)*2**15, dtype=atype)
with open("/home/ben/Desktop/tone.wav", "wb") as fh:
    fh.write(WaveHeader(len(a), 8*atype.itemsize, 1, Hz).as_bytes())
    fh.write(a.tobytes())

# stereo 32-bit floats
btype=np.dtype('<f4')
b = np.c_[np.sin(phi*taus, dtype=btype), np.sin(phi*taus/3, dtype=btype)]
with open("/home/ben/Desktop/tones.wav", "wb") as fh:
    fh.write(WaveHeader(b.shape[0], 8*btype.itemsize, b.shape[1], Hz).as_bytes())
    fh.write(b.tobytes())







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
