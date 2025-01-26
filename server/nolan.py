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
        # Step 1: Parse the MIDI file
        midi_path = "output.mid"
        score = converter.parse(midi_path)
        # Step 2: Analyze the current key
        key = score.analyze('key')
        return key

    def extract_notes_melodic_line(audio_file, time_threshold=0.2, freq_threshold=5.0):
        """
        Extract all notes from a single melodic line in a song, including rhythm information,
        while accounting for false duplicates based on time and frequency differences.
        Also filters out unnecessary sharps based on the C major scale and ensures the song ends on the dominant note.

        Parameters:
            audio_file (str): The path to the audio file.
            time_threshold (float): Minimum time difference (in seconds) to consider notes as distinct.
            freq_threshold (float): Maximum frequency difference (in Hz) to consider notes as distinct.

        Returns:
            list: A list of tuples containing the notes with their onset times and durations.
        """
        # Define C major scale notes
        c_major_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

        # Load the audio file
        y, sr = librosa.load(audio_file)

        # Detect note onsets (times when new notes start)
        onsets = librosa.onset.onset_detect(y=y, sr=sr, backtrack=False, delta=0.12, hop_length=512)
        onset_times = librosa.frames_to_time(onsets, sr=sr)

        notes_with_rhythm = []  # List to store notes with rhythm information

        for i in range(len(onsets)):
            # Define the segment for each note
            start_idx = librosa.frames_to_samples(onsets[i])
            end_idx = (
                librosa.frames_to_samples(onsets[i + 1])
                if i + 1 < len(onsets)
                else len(y)
            )
            segment = y[start_idx:end_idx]

            # Estimate pitch using librosa.pyin()
            f0, voiced_flag, _ = librosa.pyin(segment, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

            if f0 is not None:
                # Check for valid (non-NaN) pitch estimates
                if np.any(~np.isnan(f0)):  # Ensure there is at least one valid f0
                    median_f0 = np.nanmedian(f0)

                    # If conditions are met, add the note along with rhythm info
                    note = getNote(median_f0)  # Use your existing getNote function
                    if note:
                        # Calculate duration of the note
                        duration = (onset_times[i + 1] - onset_times[i]) if i + 1 < len(onset_times) else (len(segment) / sr)

                        # Check for duplicates based on time and frequency
                        is_duplicate = False
                        if notes_with_rhythm:
                            last_note, last_time, last_duration = notes_with_rhythm[-1]
                            time_diff = onset_times[i] - last_time
                            freq_diff = abs(median_f0 - librosa.note_to_hz(last_note))

                            # Check if the time difference is less than the threshold AND
                            # the frequency difference is less than the frequency threshold
                            if time_diff < time_threshold:
                                is_duplicate = True
                                # Extend the last note duration if it's a duplicate
                                new_duration = onset_times[i] + duration - last_time
                                notes_with_rhythm[-1] = (last_note, last_time, new_duration)  # Update duration of the last note

                        if not is_duplicate:
                            # Append the note, onset time, and duration
                            notes_with_rhythm.append((note, onset_times[i], duration))

        # Post-processing: Remove unnecessary sharps and filter out notes outside C2-C6 range
        processed_notes = []
        for i, (note, onset, duration) in enumerate(notes_with_rhythm):
            # Extract the octave number and clean the note (removing digits)
            octave = int(''.join(filter(str.isdigit, note))) if any(char.isdigit() for char in note) else None
            clean_note = ''.join(filter(lambda x: not x.isdigit(), note))  # Remove digits from the note

            # Filter out notes outside the C2-C6 range
            if octave is None or octave < 2 or octave >= 6:  # Change >= 6 to > 6
                continue

            # Convert sharps to natural notes
            if '#' in clean_note:
                clean_note = clean_note.replace('#', '')  # Remove the sharp

            # Allow only F# based on adjacent notes
            if note.startswith('F#'):
                keep_sharp = False
                
                # Check adjacent notes
                if i > 0:
                    prev_note = ''.join(filter(lambda x: not x.isdigit(), notes_with_rhythm[i - 1][0]))
                    if prev_note in ['F', 'G']:
                        keep_sharp = True

                if i < len(notes_with_rhythm) - 1:
                    next_note = ''.join(filter(lambda x: not x.isdigit(), notes_with_rhythm[i + 1][0]))
                    if next_note in ['F', 'G']:
                        keep_sharp = True

                if keep_sharp:
                    processed_notes.append((note, onset, duration))  # Keep the original F#
                    continue
                else:
                    # If sharp is unnecessary, we can replace F# with F
                    clean_note = 'F'

            # Append the cleaned note to processed_notes
            processed_notes.append((clean_note + (str(octave) if octave else ''), onset, duration))

        # Ensure the song ends on the dominant note
        while processed_notes and not processed_notes[-1][0].startswith(('G', 'C')):
            processed_notes.pop()
        
        
        if not processed_notes[0][0].startswith(('C')) and (processed_notes[1][0] == processed_notes[0][0]):
            processed_notes.pop(0)
            
        return processed_notes


    def play_notes_as_midi(notes, output_file="output.mid", instrument_program=0):
        """
        Convert a list of notes to a MIDI file and play it.
        The notes parameter should include tuples of (note_name, onset_time, duration).
        
        Parameters:
            notes (list): A list of tuples containing (note_name, onset_time, duration).
            output_file (str): The name of the output MIDI file.
            instrument_program (int): The MIDI program number for the instrument (0-127).
        """
        # Create a PrettyMIDI object
        midi = pretty_midi.PrettyMIDI()
        instrument = pretty_midi.Instrument(program=instrument_program)  # Use the specified instrument

        # Create MIDI notes
        for note_name, onset_time, duration in notes:
            try:
                # Convert note name (e.g., "C4") to MIDI number
                midi_number = pretty_midi.note_name_to_number(note_name)
                # Create a note and add it to the instrument
                note = pretty_midi.Note(velocity=100, pitch=midi_number, start=onset_time, end=onset_time + duration)
                instrument.notes.append(note)
            except ValueError:
                print(f"Invalid note: {note_name}")

        # Add the specified instrument to the MIDI file
        midi.instruments.append(instrument)

        # Write the MIDI file to disk
        midi.write(output_file)
        print(f"MIDI file saved as {output_file}")


    def separate_audio(audio):
        # Initialize the Spleeter separator with the 2-stems model
        separator = Separator('spleeter:2stems')

        # Provide the input file and output directory
        input_file = audio
        output_dir = 'output'

        # Separate the track
        separator.separate_to_file(input_file, output_dir)

        # Replace 'example_song.wav' with the path to your audio file
    separate_audio(file)
    file_string = file.rsplit('.', 1)[0]
    notes = extract_notes_melodic_line("output/" + file_string + "/vocals.wav")
    note_values = [note for note, _, _ in notes]
    print(f"Extracted notes: {note_values}")
    play_notes_as_midi(notes, instrument_program = 0)
    return (note_values, "output.mid")