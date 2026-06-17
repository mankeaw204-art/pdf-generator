from flask import Flask, request, send_file, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# หน้าเว็บ
HTML = """
<h2>📄 PDF Tool</h2>

<h3>1) Upload PDF</h3>
<form method="POST" action="/upload" enctype="multipart/form-data">
  <input type="file" name="file">
  <button type="submit">Upload</button>
</form>

<hr>

<h3>2) Generate PDF</h3>
<form method="POST" action="/generate">
  <input type="text" name="text" placeholder="พิมพ์ข้อความใส่ PDF">
  <button type="submit">สร้าง PDF</button>
</form>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

# -------------------------
# 📤 Upload PDF
# -------------------------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    return f"Upload สำเร็จ: {file.filename}"

# -------------------------
# ⚙️ Generate PDF
# -------------------------
@app.route("/generate", methods=["POST"])
def generate():
    from reportlab.pdfgen import canvas

    text = request.form["text"]
    output_path = os.path.join(OUTPUT_FOLDER, "output.pdf")

    c = canvas.Canvas(output_path)
    c.drawString(100, 750, text)
    c.save()

    return send_file(output_path, as_attachment=True)

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
