import math
import wave
import struct
import random

SAMPLE_RATE = 44100
DURATION = 20
VOLUME = 0.35

output_file = "sounds/brainrot.wav"

# WAV üçün nümunələr
samples = []

# Sadə beat melodiyası
notes = [
    220, 220, 330, 262,
    220, 165, 196, 220,
    330, 330, 440, 330,
    262, 220, 165, 196
]

note_duration = 0.25

for i in range(
    int(DURATION / note_duration)
):

    frequency = notes[i % len(notes)]

    start = int(
        i * note_duration * SAMPLE_RATE
    )

    end = int(
        (i + 1)
        * note_duration
        * SAMPLE_RATE
    )

    for n in range(start, end):

        t = n / SAMPLE_RATE

        # Main synth
        sound = math.sin(
            2 * math.pi * frequency * t
        )

        # İkinci komik synth
        sound += 0.35 * math.sin(
            2 * math.pi * frequency * 1.5 * t
        )

        # Kiçik "wobble" effekti
        wobble = (
            1
            + 0.25
            * math.sin(
                2 * math.pi * 5 * t
            )
        )

        sound *= wobble

        # Beat
        position = n - start

        if position < 1800:

            beat = math.exp(
                -position / 400
            )

            sound += 0.7 * beat

        # Yumşaq fade
        local = n - start

        fade_in = min(
            1,
            local / 500
        )

        fade_out = min(
            1,
            (end - n) / 500
        )

        sound *= (
            fade_in
            * fade_out
        )

        sound *= VOLUME

        # clipping
        sound = max(
            -1,
            min(1, sound)
        )

        samples.append(
            sound
        )


# =====================================================
# WAV FILE
# =====================================================

with wave.open(
    output_file,
    "w"
) as wav:

    wav.setnchannels(1)

    wav.setsampwidth(2)

    wav.setframerate(
        SAMPLE_RATE
    )

    frames = b"".join(
        struct.pack(
            "<h",
            int(
                sample * 32767
            )
        )
        for sample in samples
    )

    wav.writeframes(frames)


print()
print("🎵 Brainrot music created!")
print()
print(f"File: {output_file}")
print("Duration: 20 seconds")
print()