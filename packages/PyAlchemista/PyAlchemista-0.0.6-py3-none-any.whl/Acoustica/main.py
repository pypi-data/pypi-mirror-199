import os
import numpy as np
from scipy.io.wavfile import write

def generateTone(frequency, duration, vibrato_depth=0.2, vibrato_rate=5):
    sample_rate = 96000
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    vibrato = np.sin(2 * np.pi * vibrato_rate * t) * vibrato_depth
    waveform = np.sin(2 * np.pi * (frequency + vibrato) * t)
    scaled = np.int16(waveform * 32767)
    return scaled


def play(notes):
    sample_rate = 96000
    total_duration = sum([duration for _, duration in notes])
    waveforms = []
    for frequency, duration in notes:
        waveforms.append(generateTone(frequency, duration))
    output = np.concatenate(waveforms)
    write('/tmp/temp.wav', sample_rate, output)
    os.system(f"afplay -q 1 -t {total_duration} /tmp/temp.wav")


def getCarnaticHertz(note):
    note_hertz = {
        's': 330,
        'r1': 350,
        'r2': 370,
        'g1': 390,
        'g2': 415,
        'm1': 440,
        'm2': 465,
        'p': 495,
        'd1': 525,
        'd2': 555,
        'n1': 585,
        'n2': 615,
        'S': 660,
        'R1': 700,
        'R2': 740,
        'G1': 780,
        'G2': 830,
        'M1': 880,
        'M2': 930,
        'P': 990,
    }
    return note_hertz.get(note, None)


def getClassicalHertz(note):
    base_hertz = {
        'C': 16.35,
        'C#': 17.32,
        'D': 18.35,
        'D#': 19.45,
        'E': 20.60,
        'F': 21.83,
        'F#': 23.12,
        'G': 24.50,
        'G#': 25.96,
        'A': 27.50,
        'A#': 29.14,
        'B': 30.87,
    }
    octave = int(note[-1])
    base_note = note[:-1]
    hertz = base_hertz.get(base_note, None)
    if hertz is not None:
        return hertz * 2 ** (octave)
    else:
        return None


