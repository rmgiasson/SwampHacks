from flask import Flask, request, send_file, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
OUTPUT_FOLDER = 'outputs/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files or 'instrument' not in request.form:
            return jsonify({'error': 'Missing file or instrument'}), 400

        file = request.files['file']
        instrument = request.form['instrument']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        print(f"Description received: {instrument}")

        file_id = 'star'  # Static ID as per your requirement
        file_path_pdf = os.path.join(OUTPUT_FOLDER, f'{file_id}.pdf')
        file_path_wav = os.path.join(OUTPUT_FOLDER, f'{file_id}.wav')

        # Log paths for debugging
        print(f"Generated PDF path: {file_path_pdf}")
        print(f"Generated WAV path: {file_path_wav}")

        # Placeholder content generation (you can replace with actual file generation logic)
        with open(file_path_pdf, 'wb') as f:
            f.write(b"PDF content for 'star'")

        with open(file_path_wav, 'wb') as f:
            f.write(b"WAV content for 'star'")

        return jsonify({'message': 'star'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    try:
        # Adjusted to directly use the static 'star' file_id for testing
        if file_id != 'star':
            return jsonify({'error': 'File not found'}), 404
        
        file_path = os.path.join(OUTPUT_FOLDER, f'{file_id}')

        print(f"File requested: {file_id}")
        print(f"Checking if file exists at {file_path}")

        # Check if PDF exists
        if os.path.exists(file_path):
            print("Found PDF file!")
            return send_file(file_path, as_attachment=True)
        
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3001, debug=True)
