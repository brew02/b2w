import sys
import os
import wave
import struct

def b2w_error(message, usage):
    print(message)
    if usage == True:
        print("Usage: python3 b2w.py [file_path | directory_path]")
    sys.exit(-1)

# Binary to .wav
def b2w(file_path):
    if os.path.isfile(file_path) == False:
        return False

    # An audio file already exists
    if file_path.endswith(".wav"):
        print(F"{file_path} already exists")
        return False

    audio_path = file_path + ".wav"

    if os.path.exists(audio_path):
        print(f"{audio_path} already exists")
        return False

    with open(file_path, "br+") as file:
        content = file.read()

        channels = 1
        bits_per_sample = 16
        byte_per_bloc = channels * bits_per_sample // 8
        frequency = 44100

        content_len = len(content)
        if (content_len % 2) != 0:
            content = content + b"\x00"
            content_len = content_len + 1

        # Unpack the binary as shorts (2 bytes each)
        audio_data = struct.unpack(f"{content_len // 2}h", content[:content_len])
        
        with wave.open(audio_path, "wb") as wav_file:
            wav_file.setparams((channels, bits_per_sample // 8, frequency, 0, "NONE", "not compressed"))
            wav_file.writeframes(struct.pack(f"{len(audio_data)}h", *audio_data))

            print(f"Wrote .wav file content")

    return True

argv_len = len(sys.argv)

# We require only two arguments (the first being the name of the script, b2w.py)
if argv_len != 2:
    b2w_error(f"Invalid number of arguments: {argv_len}", True)

# Support absolute and relative paths
path = sys.argv[1]
if os.path.exists == False:
    path = os.getcwd() + path
    if os.path.exists == False:
        b2w_error(f"Invalid path: {path}", True)
    else:
        print("Using relative path")
else:
    print("Using absolute path")

if os.path.isdir(path):
    # Loop through the directory if that was specified
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        b2w(file_path)
else:
    b2w(path)

print("Converted to .wav")
