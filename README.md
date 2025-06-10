# Binary to WAV File Converter

The `b2w.py` Python script converts a raw binary, or directory of binaries, to .wav audio files. The `w2s.py` Python script converts a .wav file, or a directory of .wav files, to spectrograms.

## Prerequisites

Ensure that librosa, numpy, and matplotlib are installed using the following command:

`pip install librosa numpy matplotlib`

## Usage

`b2w.py` should be run before `w2s.py` to create the .wav files that can then be used to create the spectrograms. Instructions for running the scripts are detailed below.

### b2w.py

Run the following command, where the `file_path`/`directory_path` can be a relative or absolute path to the binary files that are to be converted to .wav files:

`python b2w.py [file_path | directory_path]`

### w2s.py

Run the following command, where the `file_path`/`directory_path` can be a relative or absolute path to the .wav files that are to be converted to spectrograms:

`python w2s.py [file_path | directory_path]`
