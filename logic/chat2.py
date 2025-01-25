import librosa
import numpy as np
from mido import Message, MidiFile, MidiTrack
from music21 import converter, midi
from scipy.io.wavfile import write
import fluidsynth
import platform
import os
import sys

os.environ['PATH'] = r"C:\\Program Files\\fluidsynth-2.4.2-winXP-x86\\lib" + ";" + os.environ['PATH']



def extract_tempo_and_intervals(audio_path):
    y, sr = librosa.load(audio_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    intervals = librosa.frames_to_time(beats, sr=sr)
    return tempo, intervals, sr

def frequency_to_note(freq):
    if freq == 0:
        return None
    A440 = 440.0
    note_number = 12 * np.log2(freq / A440) + 69
    note_number = round(note_number)
    if 21 <= note_number <= 108:
        return note_number
    return None

def note_to_frequency(note_number):
    A440 = 440.0
    return A440 * 2 ** ((note_number - 69) / 12)

def analyze_intervals(audio_path, intervals, sr):
    y, _ = librosa.load(audio_path)
    notes = []
    for i in range(len(intervals) - 1):
        start = int(intervals[i] * sr)
        end = int(intervals[i + 1] * sr)
        spectrum = np.abs(np.fft.rfft(y[start:end]))
        freqs = np.fft.rfftfreq(len(spectrum), 1 / sr)
        dominant_freq = freqs[np.argmax(spectrum)]
        note = frequency_to_note(dominant_freq)
        notes.append(note)
    return notes

def create_midi(notes, output_path):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    for note in notes:
        if note:
            track.append(Message('note_on', note=note, velocity=64, time=480))
            track.append(Message('note_off', note=note, velocity=64, time=480))
    mid.save(output_path)

# Function to convert MIDI to audio using FluidSynth
def midi_to_audio(midi_path, output_audio_path, soundfont_path="FluidR3_GM.sf2"):
    fs = fluidsynth.Synth()
    fs.sfload(soundfont_path)
    if platform.system() == 'Windows':
        fs.start(driver="directsound")
    elif platform.system() == 'Darwin':  # macOS
        fs.start(driver="coreaudio")
    else:  # For Linux or other OS
        fs.start(driver="alsa")

    # Convert the MIDI to audio
    fs.midi_to_audio(midi_path, output_audio_path)
    print(f"Audio saved to {output_audio_path}")

def generate_sheet_music(midi_path, output_path):
    # Load MIDI file using music21's converter
    try:
        score = converter.parse(midi_path)
    except Exception as e:
        print(f"Error parsing MIDI file: {e}")
        return
    
    # Save the sheet music in MusicXML format
    try:
        score.write('musicxml', output_path)
        print(f"Sheet music saved to: {output_path}")
    except Exception as e:
        print(f"Error saving sheet music: {e}")

def pianize_audio(audio_path, midi_output, sheet_output, audio_output):
    print("Extracting tempo and intervals...")
    tempo, intervals, sr = extract_tempo_and_intervals(audio_path)
    print(f"Detected Tempo: {tempo} BPM")
    
    print("Analyzing intervals...")
    notes = analyze_intervals(audio_path, intervals, sr)
    print("Detected Notes:", notes)
    
    print("Creating MIDI...")
    create_midi(notes, midi_output)
    
    print("Generating synthesized audio...")
    midi_to_audio(notes, audio_output)
    
    print("Generating sheet music...")
    generate_sheet_music(midi_output, sheet_output)
    print("Pianization complete!")

# Example usage
audio_file = "test_audio/star.wav"
midi_output = "output/pianized_song.mid"
sheet_output = "output/pianized_sheet_music.xml"
audio_output = "output/pianized_audio.wav"

pianize_audio(audio_file, midi_output, sheet_output, audio_output)
