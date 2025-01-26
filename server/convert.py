from music21 import stream, note, environment, metadata
import subprocess
import os

# Set the path to MuseScore 4
us = environment.UserSettings()
us['musescoreDirectPNGPath'] = r"C:\\Program Files\\MuseScore 4\bin\\MuseScore4.exe"

print("MuseScore path updated to:", us['musescoreDirectPNGPath'])


def create_sheet_music_from_notes(note_list, output_path):
    # Create a music21 stream
    score = stream.Stream()

    score.metadata = metadata.Metadata()
    score.metadata.title = "Skibidi Ohio"
    score.metadata.composer = "SwampHacks X"
    
    # Add notes to the stream
    for n in note_list:
        try:
            score.append(note.Note(n))
        except Exception as e:
            print(f"Error adding note {n}: {e}")
    
    # Write the sheet music to MusicXML
    musicxml_path = output_path.replace('.pdf', '.musicxml')
    try:
        score.write('musicxml', musicxml_path)
        print(f"Sheet music saved as MusicXML: {musicxml_path}")
    except Exception as e:
        print(f"Error saving sheet music as MusicXML: {e}")
        return
    
    # Use MuseScore to convert MusicXML to PDF
    try:
        subprocess.run([us['musescoreDirectPNGPath'], musicxml_path, '-o', output_path])
        print(f"Sheet music PDF saved to: {output_path}")
    except Exception as e:
        print(f"Error converting MusicXML to PDF: {e}")


# # Example usage:
# notes = ['D3', 'D3', 'E3', 'C3', 'C3', 'F#2', 'F2', 'C3', 'C3', 'D3', 'E3', 'E3', 'D3', 'E3', 'F#3', 'E3', 'D3', 'D#3', 'C3', 'A3', 'A3', 'G3', 'G3', 'E3', 'D#3', 'F3', 'E3', 'E3', 'G2', 'A2', 'G3', 'G3', 'G3', 'F3', 'F3', 'E3', 'E3', 'E3', 'E3', 'E3', 'D3', 'G#6', 'C3', 'E3', 'B2', 'C3', 'G2', 'E2', 'C#3', 'C3', 'D3', 'D3', 'E3', 'E3', 'E3', 'E3', 'E3', 'E3', 'F3', 'F3', 'E3', 'F#3', 'G3', 'A2', 'C4', 'B3', 'A3', 'G3', 'G3', 'E3', 'D3', 'C#3', 'C3', 'C3', 'D#3', 'G3', 'B3', 'C4', 'D4', 'C4', 'C4', 'C4', 'F#3', 'B3']
# output_pdf = 'bruh.pdf'
# create_sheet_music_from_notes(notes, output_pdf)
