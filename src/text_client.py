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
        text = page.get_text()
        if text.strip():
            text_lines.append(page.get_text())
        else:
            pix = page.get_pixmap()
            temp_img_path = f'/tmp/page_{page.number}.png'
            pix.save(temp_img_path)
            text_lines.append(_get_text_from_image(temp_img_path))

    return "\n".join(text_lines)


def extract_text(path):
    extension = os.path.splitext(path)[1].lower()

    if extension == ".pdf":
        return _get_text_from_pdf(path)
    elif extension in [".jpg", ".jpeg", ".png"]:
        return _get_text_from_image(path)
    else:
        raise Exception('Unsupported file!')


def translate_text(text, translator):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    translated_sentences = []
    for sentence in sentences:
        for i in range(0, len(sentence), TRANSLATOR_THRESHOLD):
            chunk = sentence[i:i + TRANSLATOR_THRESHOLD]
            translated_sentences.append(translator.ro_en.translate(chunk))

    return " ".join(translated_sentences)


def get_text_from_image(path, translator):
    text = extract_text(path)
    return translate_text(text, translator)
