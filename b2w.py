import sys
import os
import wave

def b2w_error(message, usage):
    print(message)
    if usage == True:
        print("Usage: python3 b2w.py [file_path | directory_path]")
    sys.exit(-1)

# Binary to .wav
def b2w(file_path):
    if os.path.isfile(file_path) == False:
        return False

    audio_path = file_path + ".wav"

    # An audio file already exists
    if os.path.exists(audio_path):
        return False

    with open(file_path, "br+") as file:
        content = file.read()
        with open(audio_path, "bw+") as audio_file:
            # Reference: https://en.wikipedia.org/wiki/WAV#WAV_file_header 
            WAV_HEADER_SIZE = 44

            audio_file.write("RIFF".encode("utf-8"))
            binary_size = os.fstat(file.fileno()).st_size
            wav_size = binary_size + WAV_HEADER_SIZE - 8
            audio_file.write(wav_size.to_bytes(4, byteorder="little"))
            audio_file.write("WAVE".encode("utf-8"))

            audio_file.write("fmt ".encode("utf-8"))
            # The size of the fmt block - 8
            bloc_size = 24 - 8
            audio_file.write(bloc_size.to_bytes(4, byteorder="little"))
            # PCM_INTEGER
            audio_format = 1
            audio_file.write(audio_format.to_bytes(2, byteorder="little"))

            channels = 1
            audio_file.write(channels.to_bytes(2, byteorder="little"))

            frequency = 44100
            audio_file.write(frequency.to_bytes(4, byteorder="little"))

            bits_per_sample = 16
            byte_per_bloc = channels * bits_per_sample / 8
            byte_per_sec = frequency * byte_per_bloc
            audio_file.write(byte_per_sec.to_bytes(4, byteorder="little"))
            audio_file.write(byte_per_bloc.to_bytes(2, byteorder="little"))
            audio_file.write(bits_per_sample.to_bytes(2, byteorder="little"))

            audio_file.write("data".encode("utf-8"))
            audio_file.write(binary_size.to_bytes(4, byteorder="little"))
            audio_file.truncate()

            print(f"Converted {file_path} to .wav file")
        
        with wave.open(audio_path, "wb") as wav_file:
            wav_file.writeframes(content)

            print(f"Wrote .wav file content")

    return True



argv_len = len(sys.argv)

# We require only two arguments (the first being the name of the script, b2w.py)
if argv_len != 2:
    b2w_error(f"Invalid number of arguments: {argv_len}", True)

path = sys.argv[1]
if os.path.exists == False:
    b2w_error(f"Invalid path: {path}", True)

if os.path.isdir(path):
    # Loop through the directory if that was specified
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        b2w(file_path)
else:
    b2w(path)
