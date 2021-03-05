# Copyright (C) 2021 by Landmark Acoustics LLC

import numpy as np

phi = 1000
Hz = 44100
taus = 2 * np.pi * np.linspace(0, 1, Hz, False)

# mono 16-bit integer
atype = np.dtype('<h')
a = np.array(np.sin(phi * taus)*2**15, dtype=atype)
with open("/home/ben/Desktop/tone.wav", "wb") as fh:
    fh.write(WaveHeader(len(a), 8*atype.itemsize, 1, Hz).as_bytes())
    fh.write(a.data)

# stereo 32-bit floats
btype=np.dtype('<f4')
b = np.c_[np.sin(phi*taus, dtype=btype), np.sin(phi*taus/3, dtype=btype)]
with open("/home/ben/Desktop/tones.wav", "wb") as fh:
    fh.write(WaveHeader(b.shape[0], 8*btype.itemsize, b.shape[1], Hz).as_bytes())
    fh.write(b.data)
