import fitz                 # ye pymupdf ki wajah sa aya hai or ye pdf read krta hai just
from config import collection
import nltk

nltk.download("punkt", quiet=True)            # punkt aik machine-learning model hai jo train kiya hai ye batana k lliya k kahan se sentence ko end krna chahiye
nltk.download("punkt_tab", quiet=True)  


def chunkText(text, maxWord=40, overlapSentences=1):
    sentences = nltk.sent_tokenize(text)                 # when you enter you query this line goes straight to punkt
    chunks = []
    current = []
    wordcount  = 0
    
    for sentence in sentences:
        words = len(sentence.split())
        if wordcount + words > maxWord and current:
            chunks.append(" ".join(current))
            current = current[-overlapSentences:]
            wordcount = sum(len(s.split()) for s in current)
        current.append(sentence)
        wordcount += words

    if current:
        chunks.append(" ".join(current))
    return chunks

def indexPDF(pdfPath):
    doc    = fitz.open(pdfPath)
    chunks = []
    ids    = []

    for i, page in enumerate(doc):
        text = page.get_text()

        if i > 10 and ("Notes" in text or "References" in text or "Bibliography" in text):
            print(f"Stopping at page {i+1}")
            break

        fullText   = " ".join([l.strip() for l in text.split("\n") if l.strip()])
        pageChunks = chunkText(fullText)

        for j, chunk in enumerate(pageChunks):
            if len(chunk) > 30:
                chunks.append(chunk)
                ids.append(f"page_{i+1}_chunk_{j+1}")

    collection.upsert(documents=chunks, ids=ids)
    print(f"Total chunks stored: {len(chunks)}")