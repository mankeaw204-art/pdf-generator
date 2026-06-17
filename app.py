from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import os
import time
import re

def safe_filename(name):
    # กันชื่อพัง (ไทย / เว้นวรรค / สัญลักษณ์)
    return re.sub(r'[^a-zA-Z0-9ก-๙]', '_', name)


def create_pdf_from_template(name):
    base_pdf = "templates/certificate.pdf"

    safe_name = safe_filename(name)

    output_pdf = f"outputs/{safe_name}_{int(time.time())}.pdf"
    overlay_pdf = f"outputs/overlay_{int(time.time())}.pdf"

    # 1. สร้าง layer ชื่อ
    c = canvas.Canvas(overlay_pdf)
    c.setFont("Helvetica-Bold", 30)

    # 👉 ปรับตำแหน่งชื่อ
    c.drawString(200, 400, name)

    c.save()

    # 2. เปิดไฟล์ template + overlay
    reader = PdfReader(base_pdf)
    overlay = PdfReader(overlay_pdf)

    writer = PdfWriter()

    page = reader.pages[0]

    # merge
    page.merge_page(overlay.pages[0])
    writer.add_page(page)

    # 3. save output
    with open(output_pdf, "wb") as f:
        writer.write(f)

    return output_pdf
from flask import Flask, request

app = Flask(__name__)
LINE_TOKEN = 0/qTCVIzoxV3qQSzFirHAHbQ1rz/2Npz7dclkttCLm49DUcOXAaDUZJlQSdZgkCMW2Kxc0BYlpE43chHoNrqrb9Itzu0WELZgwNmJdMxZ+H9rqthySPPCh90JOOgwgg/oavVITtbs+pPTPnp3BdkrwdB04t89/1O/w1cDnyilFU=
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(data)  # เอาไว้ดูว่ามีอะไรส่งมา

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
