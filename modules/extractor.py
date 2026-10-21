import fitz
from PIL import Image
import pytesseract


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text.strip()


def extract_text_from_image(image_path):
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text.strip()


def extract_text(file_path):

    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    return extract_text_from_image(file_path)