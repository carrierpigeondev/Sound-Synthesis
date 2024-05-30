"""
adapted from
https://stackoverflow.com/questions/9770073/sound-generation-synthesis-with-python
response by Liam
"""

import math
import pyaudio

def generate_sound(bitrate, hz, seconds):
    bitrate = max(bitrate, hz+100)
    num_frames = int(bitrate * seconds)
    rest_frames = num_frames % bitrate

    wave_data = ""

    for x in range(num_frames):
        wave_data = wave_data + chr(
            int(
                math.sin(x / ((bitrate / hz) / math.pi)) * 127 + 128
            )
        )


    for x in range(rest_frames):
        wave_data = wava_data + chr(128)

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(1),
                    channels=1,
                    rate=bitrate,
                    output=True)

    stream.write(wave_data)
    stream.stop_stream()
    stream.close()

    p.terminate()

generate_sound(16000, 500, 1)
