# from flask import Flask, request, send_file, jsonify
# import os
# from flask_cors import CORS
# from convert import create_sheet_music_from_notes
# from server.myproject.myapp.nolan import sendMidi
# import shutil

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'uploads/'
# OUTPUT_FOLDER = 'outputs/'
# PUBLIC_FOLDER = '../ui/public/'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)



# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files or 'instrument' not in request.form:
#         return jsonify({'error': 'Missing file or instrument'}), 400

#     file = request.files['file']
#     instrument = request.form['instrument']

#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(filepath)

#     print(f"Description received: {instrument}")

#     # filepath, instrument

#     # create the midi file
#     note_values, midi_path = sendMidi(filepath)

#     print('Created midi')

#     # create pdf file
#     create_sheet_music_from_notes(note_values, os.path.join(OUTPUT_FOLDER, "sheet_music.pdf"))

#     print('Made sheet music')

#     # download midi locally
#     dest_item = os.path.join(OUTPUT_FOLDER, midi_path)
#     shutil.move(midi_path, dest_item)

#     # transfer all of the shit to public
#     for item in os.listdir(OUTPUT_FOLDER):
#         src_item = os.path.join(OUTPUT_FOLDER, item)
#         dest_item = os.path.join(PUBLIC_FOLDER, item)
#         shutil.move(src_item, dest_item)
    
#     print('Finished moving')


# if __name__ == '__main__':
#     app.run(port=3001, debug=True)
