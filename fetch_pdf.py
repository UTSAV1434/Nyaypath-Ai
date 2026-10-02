import urllib.request
from pypdf import PdfReader

url = "https://www.education.gov.in/sites/upload_files/mhrd/files/upload_document/Guidelines_CSS_Scholarship.pdf"
urllib.request.urlretrieve(url, "csss_guidelines.pdf")

reader = PdfReader("csss_guidelines.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

with open("csss_guidelines.txt", "w", encoding="utf-8") as f:
    f.write(text)
