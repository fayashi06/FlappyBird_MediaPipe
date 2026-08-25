import wave
import math
import struct
import os

SAMPLE_RATE = 44100

os.makedirs("sounds", exist_ok=True)


def create_sound(filename, frequencies, duration):
    samples = int(SAMPLE_RATE * duration)

    with wave.open(
        f"sounds/{filename}",
        "w"
    ) as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        for i in range(samples):

            t = i / SAMPLE_RATE

            # Smooth fade in/out
            fade = min(
                1,
                i / 1000,
                (samples - i) / 1000
            )

            frequency = frequencies(t)

            value = int(
                16000
                * math.sin(
                    2 * math.pi * frequency * t
                )
                * fade
            )

            wav.writeframes(
                struct.pack(
                    "<h",
                    value
                )
            )


# FLAP ucun
create_sound(
    "flap.wav",
    lambda t: 700 - 300 * t,
    0.12
)


# POINT ucun
create_sound(
    "point.wav",
    lambda t: 800 + 300 * t,
    0.18
)


# HIT basi deyende yeni
create_sound(
    "hit.wav",
    lambda t: 180 - 100 * t,
    0.35
)


# COUNTDOWN(geri sayim ucun)
create_sound(
    "countdown.wav",
    lambda t: 500,
    0.20
)


# START
create_sound(
    "start.wav",
    lambda t: 500 + 600 * t,
    0.35
)


# GAME OVER
create_sound(
    "game_over.wav",
    lambda t: 500 - 350 * t,
    0.60
)



