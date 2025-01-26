from music21 import stream, note, environment, metadata
import subprocess
import os

us = environment.UserSettings()
us['musescoreDirectPNGPath'] = r"C:\\Program Files\\MuseScore 4\bin\\MuseScore4.exe" # change if needed

print("MuseScore path updated to:", us['musescoreDirectPNGPath'])


def create_sheet_music_from_notes(note_list, output_path):
    score = stream.Stream()

    score.metadata = metadata.Metadata()
    score.metadata.title = "Personal Pianist"
    score.metadata.composer = "SwampHacks X"
    
    for n in note_list:
        try:
            score.append(note.Note(n))
        except Exception as e:
            print(f"Error adding note {n}: {e}")
    
    musicxml_path = output_path.replace('.pdf', '.musicxml')
    try:
        score.write('musicxml', musicxml_path)
        print(f"Sheet music saved as MusicXML: {musicxml_path}")
    except Exception as e:
        print(f"Error saving sheet music as MusicXML: {e}")
        return
    
    try:
        subprocess.run([us['musescoreDirectPNGPath'], musicxml_path, '-o', output_path])
        print(f"Sheet music PDF saved to: {output_path}")
    except Exception as e:
        print(f"Error converting MusicXML to PDF: {e}")


