import PyPDF2

def extract_pdf_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_score(feedback_text):
    score = None
    for word in feedback_text.split():
        word = word.strip("./,")
        if word.isdigit() and 1 <= int(word) <= 10:
            score = int(word)
            break
    return score