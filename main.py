import math
import pyaudio
import wave

def create_stream(bitrate: int):
    """
    Returns a PyAudio and a stream.
    """

    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(1),
        channels=1,
        rate=bitrate,
        output=True)

    return p, stream

def close_stream(p: pyaudio.PyAudio, stream: pyaudio.Stream):
    """
    Terminates a given PyAudio and closes a given stream.
    """
    stream.stop_stream()
    stream.close()
    p.terminate()

def save_wave(filename: str, data: bytes, bitrate: int):
    """
    Saves wave data in bytes to a file at a specified bitrate.
    """
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(1)
        wf.setframerate(bitrate)
        wf.writeframes(data)

def generate_harsh(hz: int, seconds: float, bitrate: int = 16000):
    """
    Adapted from https://stackoverflow.com/questions/9770073/sound-generation-synthesis-with-python in answer from Liam.

    Generates a harsh sound at a specified frequency (`hz`) and duration (`seconds`) and returns the wave data as bytes.

    This function differs to `generate_sound()` due to it handling the `wave_data` as an ASCII string, introducing noise/unwanted audio, which can sound pretty cool.
    """
    bitrate = max(bitrate, hz + 100)
    num_frames = int(bitrate * seconds)
    rest_frames = num_frames % bitrate
    try:
        wave_data = "".join(chr(int(math.sin(x / ((bitrate / hz) / math.pi)) * 127 + 128)) for x in range(num_frames))

    except ZeroDivisionError:
        wave_data = chr(127)

    wave_data += chr(127) * rest_frames
    return wave_data.encode("utf-8")  # encoding with "latin-1" will make the sound exactly like generate_sound(), but using "utf-8" will preserve the harsh sound

def generate_sound(hz: int, seconds: float, bitrate: int = 16000):
    """
    Adapted from https://stackoverflow.com/questions/9770073/sound-generation-synthesis-with-python in answer from Liam.

    Generates a sound at a specified frequency (`hz`) and duration (`seconds`) and returns the wave data as bytes.
    """

    bitrate = max(bitrate, hz + 100)
    num_frames = int(bitrate * seconds)
    rest_frames = num_frames % bitrate
    try:
        wave_data = bytes(int(math.sin(x / ((bitrate / hz) / math.pi)) * 127 + 128) for x in range(num_frames))

    except ZeroDivisionError:
        wave_data = bytes(127)

    wave_data += bytes([127] * rest_frames)
    return wave_data

def generate_many_sounds(sounds: list[tuple[int, float]], bitrate: int = 16000, filename: str = None, harsh: bool = False):
    """
    Generates and optionally saves multiple sounds defined by a list of frequency(hz)-duration(seconds) pairs.
    Can output to both an audio stream for playback and a file.
    """
    full_wave_data = bytes()
    for hz, seconds in sounds:
        full_wave_data += generate_sound(hz, seconds, bitrate) if not harsh else generate_harsh(hz, seconds, bitrate)

    if filename is not None:
        save_wave(filename, full_wave_data, bitrate)
    else:
        p, stream = create_stream(bitrate)
        stream.write(full_wave_data)
        close_stream(p, stream)

if __name__ == "__main__":
    sounds = [
        (500, 0.1),
        (600, 0.1),
        (700, 0.1),
        (600, 0.1),
        (500, 0.1)
    ]

    generate_many_sounds(sounds, filename="ouput.wav", harsh=True)
