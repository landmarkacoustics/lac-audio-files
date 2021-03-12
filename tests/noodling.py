# Copyright (C) 2021 by Landmark Acoustics LLC

from lacaudiofiles.wave import WaveHeader
import struct

fmt = WaveHeader.binary_format()

N = struct.calcsize(fmt)

binaries = {}

files = {
    'chirp': 'excerpt from TRES Unit5 09 1999.wav',
    'mono': 'tone.wav',
    'tones': 'tones.wav',
}

for k, v in files.items():
    with open('/'.join(['/home/ben/Desktop', v]), 'rb') as fh:
        binaries[k] = fh.read(N)

print('binaries:')
print(binaries)

structs = {k: struct.unpack(fmt, v) for k, v in binaries.items()}

headers = {k: WaveHeader.unpack(v) for k, v in binaries.items()}

print('headers:')
for k, v in headers.items():
    print(k)
    print(v._wave.values())
    print(v._format.values())
    print(v._data.values())

