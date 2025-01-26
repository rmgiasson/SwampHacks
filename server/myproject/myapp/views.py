# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import os
import shutil
from .convert import create_sheet_music_from_notes
from .nolan import sendMidi

UPLOAD_FOLDER = 'uploads/'
OUTPUT_FOLDER = 'outputs/'
PUBLIC_FOLDER = '../../ui/public/'

# Ensure these directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@csrf_exempt
def upload_file(request):
    print('Reached Here')
    if request.method == 'POST':
        if 'file' not in request.FILES or 'instrument' not in request.POST:
            return JsonResponse({'error': 'Missing file or instrument'}, status=400)

        file = request.FILES['file']
        instrument = request.POST['instrument']

        if file.name == '':
            return JsonResponse({'error': 'No selected file'}, status=400)
        
        print('------------------> ', file.name)

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        fs = FileSystemStorage(location=UPLOAD_FOLDER)
        filepath = fs.save(file.name, file)
        filepath = os.path.join('../myproject/uploads', filepath)
        print(filepath, '<-----------------')

        # Create the midi file
        note_values, midi_path = sendMidi(filepath, instrument)

        # Create sheet music PDF
        create_sheet_music_from_notes(note_values, os.path.join(OUTPUT_FOLDER, "sheet_music.pdf"))

        # Move MIDI file to the outputs folder
        dest_item = os.path.join(OUTPUT_FOLDER, midi_path)
        shutil.move(midi_path, dest_item)

        # Move all files from the outputs folder to the public folder
        for item in os.listdir(OUTPUT_FOLDER):
            src_item = os.path.join(OUTPUT_FOLDER, item)
            dest_item = os.path.join(PUBLIC_FOLDER, item)
            shutil.move(src_item, dest_item)

        return JsonResponse({'message': 'Files processed successfully'})

    return JsonResponse({'error': 'Invalid method'}, status=405)
