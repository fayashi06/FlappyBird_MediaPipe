import wave
import math
import struct
import os

os.makedirs("sounds", exist_ok=True)

sample_rate = 44100
duration = 0.18

frequencies = [900, 1300]

samples = []

for i in range(int(sample_rate * duration)):

    t = i / sample_rate

    freq = frequencies[0] if t < duration / 2 else frequencies[1]

    envelope = 1 - (t / duration)

    value = (
        math.sin(2 * math.pi * freq * t)
        * envelope
        * 0.45
    )

    samples.append(
        int(value * 32767)
    )

with wave.open(
    "sounds/coin.wav",
    "w"
) as wav:

    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)

    wav.writeframes(
        b"".join(
            struct.pack("<h", sample)
            for sample in samples
        )
    )

print("coin.wav created successfully!")