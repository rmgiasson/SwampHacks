from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
OUTPUT_FOLDER = 'outputs/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the post request has the file part
        if 'file' not in request.files or 'instrument' not in request.form:
            return jsonify({'error': 'Missing file or instrument'}), 400

        file = request.files['file']
        instrument = request.form['instrument']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Process the string (description) as needed (placeholder here)
        print(f"Description received: {instrument}")

        return jsonify({'message': 'File and description received successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_path_pdf = os.path.join(OUTPUT_FOLDER, filename + '.pdf')
        file_path_wav = os.path.join(OUTPUT_FOLDER, filename + '.wav')

        if os.path.exists(file_path_pdf) and os.path.exists(file_path_wav):
            return send_file(file_path_pdf, as_attachment=True)

        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3001, debug=True)
