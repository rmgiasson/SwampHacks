import subprocess
from music21 import converter

def midi_to_musicxml(midi_path, musicxml_path):
    """Convert MIDI file to MusicXML format."""
    try:
        # Parse the MIDI file
        score = converter.parse(midi_path)
        
        # Write the score to MusicXML
        score.write('musicxml', fp=musicxml_path)
        print(f"MusicXML saved to: {musicxml_path}")
    
    except Exception as e:
        print(f"Error converting MIDI to MusicXML: {e}")


def musicxml_to_pdf(musicxml_path, pdf_path):
    """Convert MusicXML file to PDF using MuseScore CLI."""
    try:
        # Call MuseScore CLI to convert MusicXML to PDF
        subprocess.run(['musescore', musicxml_path, '-o', pdf_path], check=True)
        print(f"PDF saved to: {pdf_path}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error converting MusicXML to PDF: {e}")


def midi_to_pdf(midi_path, pdf_path):
    """Convert MIDI file directly to PDF sheet music."""
    try:
        # Convert MIDI to MusicXML
        musicxml_path = 'temp.musicxml'
        midi_to_musicxml(midi_path, musicxml_path)
        
        # Convert MusicXML to PDF
        musicxml_to_pdf(musicxml_path, pdf_path)
        print(f"Sheet music PDF created: {pdf_path}")
    
    except Exception as e:
        print(f"Error in conversion pipeline: {e}")


# Example usage
midi_to_pdf('penes.mid', 'penes.pdf')
