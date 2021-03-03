# lac-audio-files
**Reading and writing audio files in Python**

The modules in the Python Standard Library and in SciPy don't suit my needs.
The [`wave`][1] package in the Standard Library is terrible.
It assumes a lot of defaults about the format of the audio data, and doesn't
let you change any of them.
The [`io`][2] package in SciPy takes whole arrays at once, but I need
incremental io.

[1]: https://docs.python.org/3.8/library/wave.html
[2]: https://docs.scipy.org/doc/scipy/reference/io.html
