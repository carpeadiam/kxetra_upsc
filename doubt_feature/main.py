import os
from flask import Flask
from model import model
from upload import upload_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(model, url_prefix='/model')
app.register_blueprint(upload_bp, url_prefix='/upload')

# Route to home page
@app.route('/')
def index():
    return "Math Problem Solver - Access the interface at /upload/page"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)