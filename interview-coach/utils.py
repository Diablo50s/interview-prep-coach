import re
import PyPDF2


def extract_pdf_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text


def extract_score(feedback_text):
    """Read the 'Score: X/10' line. Returns None if the model didn't give one."""
    match = re.search(r"Score:\s*\**\s*(\d{1,2})\s*/\s*10", feedback_text, re.IGNORECASE)
    if match:
        score = int(match.group(1))
        if 0 <= score <= 10:
            return score
    return None
