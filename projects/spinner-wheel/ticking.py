import math
import wave
import struct

# ========================
# Configuration
# ========================
FILENAME = "spin_ticks.wav"
SAMPLE_RATE = 44100
DURATION = 4.6          # total length in seconds
TICK_DURATION = 0.025   # length of a single tick (25 ms)
TICK_FREQ = 1400        # Hz
VOLUME = 0.8

START_TICKS_PER_SEC = 18
END_TICKS_PER_SEC = 2

# ========================
# Helpers
# ========================
def ease_out(t):
    """Ease-out curve: fast -> slow"""
    return 1 - (1 - t) ** 3

# ========================
# Create empty buffer
# ========================
num_samples = int(SAMPLE_RATE * DURATION)
buffer = [0.0] * num_samples

# ========================
# Schedule ticks
# ========================
time = 0.0
while time < DURATION:
    progress = time / DURATION
    eased = ease_out(progress)

    ticks_per_sec = (
        START_TICKS_PER_SEC * (1 - eased) +
        END_TICKS_PER_SEC * eased
    )

    interval = 1 / ticks_per_sec

    start_sample = int(time * SAMPLE_RATE)
    tick_samples = int(TICK_DURATION * SAMPLE_RATE)

    for i in range(tick_samples):
        idx = start_sample + i
        if idx >= num_samples:
            break

        t = i / SAMPLE_RATE

        # Click waveform with fast decay
        sample = math.sin(2 * math.pi * TICK_FREQ * t)
        envelope = math.exp(-80 * t)

        buffer[idx] += sample * envelope * VOLUME

    time += interval

# ========================
# Normalize
# ========================
max_amp = max(abs(s) for s in buffer)
if max_amp > 0:
    buffer = [s / max_amp for s in buffer]

# ========================
# Write WAV file
# ========================
with wave.open(FILENAME, "w") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SAMPLE_RATE)

    for sample in buffer:
        wav.writeframes(struct.pack("<h", int(sample * 32767)))

print(f"Generated {FILENAME}")
