from flask import Flask, request
import requests
from reportlab.pdfgen import canvas
import os
import json

app = Flask(__name__)

LINE_TOKEN = "ใส่ Channel Access Token ตรงนี้"

OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ---------------------------
# ฟังก์ชันส่งข้อความกลับ LINE
# ---------------------------
def reply_text(reply_token, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers=headers,
        data=json.dumps(data)
    )


# ---------------------------
# ฟังก์ชันส่งไฟล์ PDF
# ---------------------------
def push_pdf(user_id, file_path):
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    files = {
        "file": open(file_path, "rb")
    }

    data = {
        "message": "📄 นี่คือไฟล์ PDF ของคุณ"
    }

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        data=data,
        files=files
    )


# ---------------------------
# สร้าง PDF จากชื่อ
# ---------------------------
def create_pdf(name):
    file_path = os.path.join(OUTPUT_FOLDER, f"{name}.pdf")

    c = canvas.Canvas(file_path)

    c.setFont("Helvetica-Bold", 24)
    c.drawString(200, 800, "CERTIFICATE")

    c.setFont("Helvetica", 18)
    c.drawString(200, 750, f"Name: {name}")

    c.setFont("Helvetica-Oblique", 12)
    c.drawString(200, 700, "Generated automatically by system")

    c.save()

    return file_path


# ---------------------------
# LINE Webhook
# ---------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json

    event = body["events"][0]
    reply_token = event["replyToken"]
    message = event["message"]["text"]

    user_id = event["source"]["userId"]

    # 🧠 เอาข้อความ = ชื่อ
    name = message

    # 🧾 สร้าง PDF
    file_path = create_pdf(name)

    # 💬 ตอบกลับ
    reply_text(reply_token, f"กำลังสร้าง PDF ของ {name}...")

    # 📤 ส่ง PDF กลับ
    push_pdf(user_id, file_path)

    return "OK"


# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
