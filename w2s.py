import librosa
import numpy
import matplotlib.pyplot as plt

import sys
import os

cwd = os.getcwd()

def w2s_error(message, usage):
    print(message)
    if usage == True:
        print("Usage: python3 w2s.py [file_path | directory_path]")
    sys.exit(-1)

# .wav to spectrogram
def w2s(audio_path):
    if os.path.isfile(audio_path) == False:
        return False

    if audio_path.endswith(".wav") == False:
        return False

    index = audio_path.rfind("\\")
    if index == -1:
        return False
    
    audio_name = audio_path[(index + 1):]
    audio_name = audio_name.replace(".wav", "")
    spec_path = f"{cwd}\\specs\\{audio_name}.png"
    if os.path.exists(spec_path):
        print(f"{spec_path} already exists")
        return False

    y, sr = librosa.load(audio_path)
    spec = numpy.abs(librosa.stft(y=y))
    spec_db = librosa.power_to_db(spec, ref=numpy.median)
    plt.ioff()
    plt.figure(figsize=(10, 4))
    plt.ylim((0, 11000))
    librosa.display.specshow(spec_db, sr=sr, x_axis="time", y_axis="hz")
    plt.colorbar(format="%+2.0f dB")
    plt.tight_layout()

    plt.savefig(spec_path, transparent=True, format="png")

    plt.close()
    return True

argv_len = len(sys.argv)

# We require two arguments (the first being the name of the script, b2w.py)
if argv_len != 2:
    w2s_error(f"Invalid number of arguments: {argv_len}", True)

# Support absolute and relative paths
path = sys.argv[1]
if os.path.exists == False:
    path = os.getcwd() + path
    if os.path.exists == False:
        w2s_error(f"Invalid path: {path}", True)
    else:
        print("Using relative path")
else:
    print("Using absolute path")

os.makedirs("specs", exist_ok=True)

if os.path.isdir(path):
    # Loop through the directory if that was specified
    for file_name in os.listdir(path):
        w2s(os.path.join(path, file_name))
else:
    w2s(path)

print("Created spectrograms")
