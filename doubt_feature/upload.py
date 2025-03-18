from flask import Blueprint, request, jsonify, Flask, render_template
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import base64
from PIL import Image

#upload_bp = Blueprint("upload", __name__)
upload_bp = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route("/page")
def page():
    return render_template("index.html")

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Secure filename and save
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    # Rename the file to doubt.jpg
    new_file_path = os.path.join(UPLOAD_FOLDER, "doubt.jpg")
    os.rename(file_path, new_file_path)
    
    return jsonify({"message": "File uploaded successfully", "filename": "doubt.jpg"})

if __name__ == "__main__":
     upload_bp.run()
