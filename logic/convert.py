from music21 import stream, note, environment, metadata

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
    
    # Save the sheet music as PDF
    try:
        score.write('musicxml.pdf', output_path)
        print(f"Sheet music PDF saved to: {output_path}")
    except Exception as e:
        print(f"Error saving sheet music as PDF: {e}")

# Example usage:
notes = ['C4', 'D4', 'E4', 'F4', 'G4']
output_pdf = 'sheet_music_notes.pdf'
create_sheet_music_from_notes(notes, output_pdf)