import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from all pages of a PDF using pdfplumber."""
    text=""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def tokenize_text(text: str):
    """Tokenize text into sentences using spaCy."""
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]


# if __name__ == "__main__":
#     text = extract_text_from_pdf("./materials/IAS Notes.pdf")
#     print("First 1000 characters:\n", text[:1000])

#     sentences = tokenize_text(text)
#     print("\nFirst 5 sentences:")
#     for sentence in sentences[:5]:
#         print("-", sentence)