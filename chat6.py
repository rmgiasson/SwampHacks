import librosa
import numpy as np
from mido import Message, MidiFile, MidiTrack
from music21 import converter, midi
from scipy.io.wavfile import write
from spleeter.separator import Separator
import librosa.display

file_name = "drugs"


def extract_tempo_and_intervals(audio_path):
    y, sr = librosa.load(audio_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
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
        # Use Harmonic/Percussive Source Separation for better pitch tracking
        y_harmonic, y_percussive = librosa.effects.hpss(y[start:end])
        # Apply the PYIN pitch detection algorithm
        pitches, magnitudes = librosa.pyin(y_harmonic, fmin=librosa.note_to_hz('C1'), fmax=librosa.note_to_hz('B8'))
        if pitches is not None:
            avg_pitch = np.nanmean(pitches)
            note = frequency_to_note(avg_pitch)
            notes.append(note)
    return notes

def create_midi(notes, output_path, tempo=120):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    for note in notes:
        if note:
            track.append(Message('note_on', note=note, velocity=64, time=480))
            track.append(Message('note_off', note=note, velocity=64, time=480))
    # Set the tempo to match the detected tempo
    track.append(midi.MetaMessage('set_tempo', tempo=librosa.beat.tempo_to_bpm(tempo)))
    mid.save(output_path)

def generate_synthesized_audio(notes, output_audio_path, sr=44100, duration=0.5):
    audio = np.zeros(0)
    for note in notes:
        if note is None:
            silence = np.zeros(int(sr * duration))
            audio = np.concatenate((audio, silence))
        else:
            freq = note_to_frequency(note)
            t = np.linspace(0, duration, int(sr * duration), endpoint=False)
            tone = (
                np.sin(2 * np.pi * freq * t) + 
                0.5 * np.sin(2 * np.pi * 2 * freq * t) +
                0.25 * np.sin(2 * np.pi * 3 * freq * t)
            )
            tone *= np.exp(-3 * t)
            audio = np.concatenate((audio, tone))
    audio = audio / np.max(np.abs(audio))
    write(output_audio_path, sr, (audio * 32767).astype(np.int16))

def generate_sheet_music(midi_path, output_path):
    try:
        score = converter.parse(midi_path)
    except Exception as e:
        print(f"Error parsing MIDI file: {e}")
        return
    
    try:
        score.write('musicxml', output_path)
        print(f"Sheet music saved to: {output_path}")
    except Exception as e:
        print(f"Error saving sheet music: {e}")

# Use Spleeter to separate vocals and accompaniment
def separate_vocals_and_accompaniment(audio_path, output_path_accomp):
    separator = Separator('spleeter:2stems')  # 2 stems: vocals, accompaniment
    separator.separate_to_file(audio_path, output_path_accomp)
    print(f"Separation complete. Accompaniment saved to {output_path_accomp}")

def pianize_audio(audio_path, midi_output, sheet_output, audio_output, separated_audio_output):
    print("Separating vocals and accompaniment...")
    separate_vocals_and_accompaniment(audio_path, separated_audio_output)

    # Load the separated accompaniment audio file
    accompaniment_audio_path = f"output/separated_audio/{file_name}/accompaniment.wav"
    tempo, intervals, sr = extract_tempo_and_intervals(accompaniment_audio_path)
    print(f"Detected Tempo: {tempo} BPM")
    
    print("Analyzing intervals...")
    notes = analyze_intervals(accompaniment_audio_path, intervals, sr)
    print("Detected Notes:", notes)
    
    print("Creating MIDI...")
    create_midi(notes, midi_output, tempo)
    
    print("Generating synthesized audio...")
    generate_synthesized_audio(notes, audio_output)
    
    print("Generating sheet music...")
    generate_sheet_music(midi_output, sheet_output)
    print("Pianization complete!")

if __name__ == "__main__":
    # Example usage
    
    audio_file = f"test_audio/{file_name}.wav"
    midi_output = "output/pianized_song.mid"
    sheet_output = "output/pianized_sheet_music.xml"
    audio_output = "output/pianized_audio.wav"
    separated_audio_output = "output/separated_audio"

    pianize_audio(audio_file, midi_output, sheet_output, audio_output, separated_audio_output)
