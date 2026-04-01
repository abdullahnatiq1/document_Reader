import fitz                 # ye pymupdf ki wajah sa aya hai or ye pdf read krta hai just
from config import collection


def chunkText(text, chunkSize=500, overlap=100):
    chunks = []
    start  = 0
    while start < len(text):
        end = start + chunkSize
        chunks.append(text[start:end])
        start = end - overlap
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
        pageChunks = chunkText(fullText, chunkSize=500, overlap=100)

        for j, chunk in enumerate(pageChunks):
            if len(chunk) > 30:
                chunks.append(chunk)
                ids.append(f"page_{i+1}_chunk_{j+1}")

    collection.upsert(documents=chunks, ids=ids)
    print(f"Total chunks stored: {len(chunks)}")