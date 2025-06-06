import img2pdf
import os

def images_to_pdf(image_paths, pdf_path):
    # 支持多种输入格式
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))