from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if not text.strip():
            return "ERROR: Unable to extract text from this PDF. Scanned/image PDFs are not supported in the MVP."
        return text
    except Exception as e:
        return f"ERROR: Unable to extract text from this PDF. {str(e)}"
