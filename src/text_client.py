import os.path
import spacy

import fitz
from paddleocr import PaddleOCR

TRANSLATOR_THRESHOLD = 4999

ocr = PaddleOCR(lang="ro")
nlp = spacy.load("ro_core_news_sm")


def _get_text_from_image(path):
    result = ocr.predict(input=path)
    text_lines = []

    for res in result:
        lines = res.get("rec_texts")
        text_lines.extend(lines)

    return "\n".join(text_lines)


def _get_text_from_pdf(path):
    doc = fitz.open(path)
    text_lines = []

    for page in doc:
        text_lines.append(page.get_text())

    return "\n".join(text_lines)


def get_text_from_image(path, translator):
    extension = os.path.splitext(path)[1].lower()

    if extension == ".pdf":
        text = _get_text_from_pdf(path)
    elif extension in [".jpg", ".jpeg", ".png"]:
        text = _get_text_from_image(path)
    else:
        raise Exception('Unsupported file!')

    doc = nlp(text)

    translated = ""
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    for s in sentences:
        r = len(sentences) // TRANSLATOR_THRESHOLD + 1

        for i in range(r):
            start = i * TRANSLATOR_THRESHOLD
            end = start + TRANSLATOR_THRESHOLD
            segment_ro = s[start:end]
            segment_en = translator.translate(segment_ro)
            translated += segment_en

    return translated
