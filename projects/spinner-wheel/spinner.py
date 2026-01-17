import math
import wave
import struct

# Output file
filename = "tick.wav"

# Audio settings
sample_rate = 44100  # CD-quality
duration = 0.03      # 30 ms tick
frequency = 1200     # Hz (clicky, not boomy)
volume = 0.8

num_samples = int(sample_rate * duration)

with wave.open(filename, "w") as wav_file:
    wav_file.setnchannels(1)       # mono
    wav_file.setsampwidth(2)       # 16-bit
    wav_file.setframerate(sample_rate)

    for i in range(num_samples):
        t = i / sample_rate

        # Sine wave
        sample = math.sin(2 * math.pi * frequency * t)

        # Exponential decay envelope
        envelope = math.exp(-60 * t)

        value = int(sample * envelope * volume * 32767)
        wav_file.writeframes(struct.pack("<h", value))

print(f"Generated {filename}")
