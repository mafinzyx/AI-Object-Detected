from flask import Blueprint, request, jsonify, send_file, url_for
import os
from werkzeug.utils import secure_filename
from .models.image_processor import ImageProcessor
from flask import render_template

main = Blueprint('main', __name__)
image_processor = ImageProcessor()

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process image and get detected objects
        objects = image_processor.detect_objects(filepath)
        return jsonify({
            'message': 'File uploaded successfully',
            'objects': objects,
            'filename': filename
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@main.route('/highlight', methods=['POST'])
def highlight_object():
    data = request.json
    if not data or 'filename' not in data or 'object_name' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    filename = data['filename']
    object_name = data['object_name']
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(filepath):
        print(f"[highlight] File not found: {filepath}")
        return jsonify({'error': 'File not found'}), 404
    
    try:
        print(f"[highlight_object] Called for {filepath} and object '{object_name}'")
        # Process image and highlight the requested object
        result_path = image_processor.highlight_object(filepath, object_name)
        if result_path and os.path.exists(result_path):
            print(f"[highlight] Sending file: {result_path}")
            relative_path = os.path.relpath(result_path, 'app/static')
            image_url = url_for('static', filename=relative_path)
            return jsonify({'image_url': image_url})
        else:
            print(f"[highlight] Object '{object_name}' not found in {filepath}")
            return jsonify({'error': f"Object '{object_name}' not found"}), 404
    except Exception as e:
        print(f"[highlight] Internal error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500 