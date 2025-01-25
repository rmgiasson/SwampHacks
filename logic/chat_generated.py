import fluidsynth
from spleeter.separator import Separator
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import butter, lfilter
from music21 import converter, midi

# Function to convert MIDI to audio using FluidSynth
def midi_to_audio(midi_path, output_audio_path, soundfont_path="FluidR3_GM.sf2"):
    fs = fluidsynth.Synth()
    fs.sfload(soundfont_path)
    fs.start(driver="alsa")  # Adjust depending on your OS

    # Convert the MIDI to audio
    fs.midi_to_audio(midi_path, output_audio_path)
    print(f"Audio saved to {output_audio_path}")

# Function to separate tracks using Spleeter
def separate_tracks(audio_path, output_dir="output"):
    separator = Separator('spleeter:2stems')  # Separate into two stems: vocals and accompaniment
    separator.separate_to_file(audio_path, output_dir)
    print(f"Tracks separated. Output saved to {output_dir}")

# Function to apply a band-pass filter to the audio (optional)
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

# Main function to process the MIDI and audio
def process_audio(midi_file, midi_audio_output, soundfont_path, audio_file=None, lowcut=None, highcut=None):
    # Step 1: Convert MIDI to Audio using FluidSynth
    midi_to_audio(midi_file, midi_audio_output, soundfont_path)

    # Step 2: If a mixed audio file is provided, separate tracks using Spleeter
    if audio_file:
        print("Separating audio tracks...")
        separate_tracks(audio_file, "output")

        # Optionally apply a band-pass filter if lowcut and highcut frequencies are specified
        if lowcut and highcut:
            print("Applying band-pass filter...")
            # Load the audio that Spleeter separated (assuming 'accompaniment.wav' is the main track)
            # You'll want to load the audio file for filtering and then save the result
            from scipy.io.wavfile import read
            sr, data = read("output/" + audio_file.split("/")[-1].split(".")[0] + "/accompaniment.wav")
            filtered_data = bandpass_filter(data, lowcut, highcut, sr)
            write("output/filtered_accompaniment.wav", sr, filtered_data)
            print("Filtered audio saved to 'output/filtered_accompaniment.wav'")
    
    print("Processing complete!")

# Example usage:
midi_file = "output/pianized_song.mid"  # Path to your MIDI file
midi_audio_output = "output/pianized_audio.wav"  # Path where the MIDI audio will be saved
soundfont_path = "path/to/your/soundfont.sf2"  # Path to a SoundFont file for FluidSynth
audio_file = "test_audio/star.wav"  # Path to the mixed audio file you want to separate (optional)

# Optional band-pass filter parameters:
lowcut = 100.0  # Low frequency cutoff (Hz)
highcut = 1000.0  # High frequency cutoff (Hz)

# Run the audio processing
process_audio(midi_file, midi_audio_output, soundfont_path, audio_file, lowcut, highcut)
