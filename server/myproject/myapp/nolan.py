import librosa
import numpy as np
import pretty_midi
import matplotlib.pyplot as plt
from spleeter.separator import Separator
from music21 import converter, note, stream, midi, interval

def sendMidi(file, instrument = 'piano'):

    def getNote(frequency):
        if frequency <= 0:
            return None  
        midi = round(69 + 12 * np.log2(frequency / 440.0))
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note = notes[midi % 12] + str(midi // 12 - 1)  
        return note

    def getKey():
        midi_path = "output.mid"
        score = converter.parse(midi_path)
        key = score.analyze('key')
        return key

    def extract_notes_melodic_line(audio_file, time_threshold=0.2, freq_threshold=5.0):
        c_major_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

        y, sr = librosa.load(audio_file)

        onsets = librosa.onset.onset_detect(y=y, sr=sr, backtrack=False, delta=0.12, hop_length=512)
        onset_times = librosa.frames_to_time(onsets, sr=sr)

        notes_with_rhythm = []  

        for i in range(len(onsets)):
            start_idx = librosa.frames_to_samples(onsets[i])
            end_idx = (
                librosa.frames_to_samples(onsets[i + 1])
                if i + 1 < len(onsets)
                else len(y)
            )
            segment = y[start_idx:end_idx]

            f0, voiced_flag, _ = librosa.pyin(segment, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

            if f0 is not None:
                if np.any(~np.isnan(f0)): 
                    median_f0 = np.nanmedian(f0)

                    note = getNote(median_f0)  
                    if note:
                        duration = (onset_times[i + 1] - onset_times[i]) if i + 1 < len(onset_times) else (len(segment) / sr)

                        is_duplicate = False
                        if notes_with_rhythm:
                            last_note, last_time, last_duration = notes_with_rhythm[-1]
                            time_diff = onset_times[i] - last_time
                            freq_diff = abs(median_f0 - librosa.note_to_hz(last_note))

                            if time_diff < time_threshold:
                                is_duplicate = True
                                new_duration = onset_times[i] + duration - last_time
                                notes_with_rhythm[-1] = (last_note, last_time, new_duration) 

                        if not is_duplicate:
                            notes_with_rhythm.append((note, onset_times[i], duration))

        processed_notes = []
        for i, (note, onset, duration) in enumerate(notes_with_rhythm):
            octave = int(''.join(filter(str.isdigit, note))) if any(char.isdigit() for char in note) else None
            clean_note = ''.join(filter(lambda x: not x.isdigit(), note)) 

            if octave is None or octave < 2 or octave >= 6: 
                continue

            if '#' in clean_note:
                clean_note = clean_note.replace('#', '') 

            if note.startswith('F#'):
                keep_sharp = False
                
                if i > 0:
                    prev_note = ''.join(filter(lambda x: not x.isdigit(), notes_with_rhythm[i - 1][0]))
                    if prev_note in ['F', 'G']:
                        keep_sharp = True

                if i < len(notes_with_rhythm) - 1:
                    next_note = ''.join(filter(lambda x: not x.isdigit(), notes_with_rhythm[i + 1][0]))
                    if next_note in ['F', 'G']:
                        keep_sharp = True

                if keep_sharp:
                    processed_notes.append((note, onset, duration))  
                    continue
                else:
                    clean_note = 'F'

            processed_notes.append((clean_note + (str(octave) if octave else ''), onset, duration))

        while processed_notes and not processed_notes[-1][0].startswith(('G', 'C')):
            processed_notes.pop()
        
        
        if not processed_notes[0][0].startswith(('C')) and (processed_notes[1][0] == processed_notes[0][0]):
            processed_notes.pop(0)
            
        return processed_notes


    def play_notes_as_midi(notes, output_file="output.mid", instrument_program=57):
        midi = pretty_midi.PrettyMIDI()
        instrument = pretty_midi.Instrument(program=instrument_program)

        for note_name, onset_time, duration in notes:
            try:
                midi_number = pretty_midi.note_name_to_number(note_name)
                note = pretty_midi.Note(velocity=100, pitch=midi_number, start=onset_time, end=onset_time + duration)
                instrument.notes.append(note)
            except ValueError:
                print(f"Invalid note: {note_name}")

        midi.instruments.append(instrument)

        midi.write(output_file)
        print(f"MIDI file saved as {output_file}")


    def separate_audio(audio):
        separator = Separator('spleeter:2stems')

        input_file = audio
        output_dir = '../myproject/output'

        print(input_file)
        separator.separate_to_file(input_file, output_dir)

    separate_audio(file)
    file_string = file.rsplit('.', 1)[0]
    last_backslash_index = file_string.rfind("\\")
    file_string = file_string[last_backslash_index + 1:]

    notes = extract_notes_melodic_line(f"../myproject/output/{file_string}/vocals.wav")
    note_values = [note for note, _, _ in notes]
    print(f"Extracted notes: {note_values}")
    play_notes_as_midi(notes, instrument_program = 0)
    return (note_values, "output.mid")