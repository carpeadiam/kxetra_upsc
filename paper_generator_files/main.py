from flask import Blueprint,Flask
from chat1 import gemini
from pdf_creator import qp_pdf

app = Flask(__name__)

def create_gemini_app():
    app = Flask(__name__)
    app.register_blueprint(gemini, url_prefix='/api')
    return app 

def create_qp_pdf_app():
    app = Flask(__name__)
    app.register_blueprint(qp_pdf, url_prefix='/pdf')
    return app

if __name__ == "__main__":
    gemini_app = create_gemini_app()
    qp_pdf_app = create_qp_pdf_app()

    gemini_app.run(port = 5001)
    #qp_pdf_app.run(port = 5002)