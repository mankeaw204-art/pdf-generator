from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import os

def create_pdf_from_template(name):
    base_pdf = "templates/certificate.pdf"
    output_pdf = f"outputs/{name}.pdf"
    overlay_pdf = "outputs/overlay.pdf"

    # 1. สร้างข้อความ (ชื่อ)
    c = canvas.Canvas(overlay_pdf)
    c.setFont("Helvetica-Bold", 30)

    # 👉 ตำแหน่งชื่อ (ปรับได้ทีหลัง)
    c.drawString(200, 400, name)

    c.save()

    # 2. เอามาซ้อนกับ template
    reader = PdfReader(base_pdf)
    overlay = PdfReader(overlay_pdf)

    writer = PdfWriter()

    page = reader.pages[0]
    page.merge_page(overlay.pages[0])
    writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    return output_pdf
