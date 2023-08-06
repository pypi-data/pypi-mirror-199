# pm-process-video

[![PyPI - Version](https://img.shields.io/pypi/v/pm-process-video.svg)](https://pypi.org/project/pm-process-video)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pm-process-video.svg)](https://pypi.org/project/pm-process-video)

-----

## Installation

```console
pipx install pm-process-video
```

Then run:

```console
process_video my_file.vtt
```

This package is installed under the `pm` package namespace.
To use it in Python code import like this:

```python
from pm.process_video import vtt_to_text
```

## Usage

Running this:

```console
process_video "My video file.mkv"
```

Will normalize the audio, transcribe using Open AI's whisper, and save the file, transcription, and text transcript in `~/Documents/screencast/encoded`.
You can customize the target directory with the `--target-dir` option.

## Publish

To try out the current implementation without building:

```console
hatch run process_video ...
```

To build and publish:

```console
hatch build
hatch publish
```

## License

`pm-process-video` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
