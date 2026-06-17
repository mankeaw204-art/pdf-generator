from flask import Flask, request, send_file
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "PDF Generator is running!"

@app.route("/generate", methods=["POST"])
def generate_pdf():
    data = request.json
    text = data.get("text", "Hello PDF!")

    file_path = "output.pdf"
    c = canvas.Canvas(file_path)
    c.drawString(100, 750, text)
    c.save()

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
