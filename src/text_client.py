import os.path
import spacy

import fitz
from paddleocr import PaddleOCR

TRANSLATOR_THRESHOLD = 4999

_ocr = None
_nlp = None

def get_ocr():
    global _ocr

    if _ocr is None:
        _ocr = PaddleOCR(lang="ro")
    return _ocr

def get_nlp():
    global _nlp

    if _nlp is None:
        _nlp = spacy.load("ro_core_news_sm")
    return _nlp


def _get_text_from_image(path):
    result = get_ocr().predict(input=path)
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
            try:
                pix.save(temp_img_path)
                text_lines.append(_get_text_from_image(temp_img_path))
            finally:
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)

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
    doc = get_nlp()(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    translated_chunks = []
    batch = []
    batch_length = 0

    for sentence in sentences:
        if len(sentence) > TRANSLATOR_THRESHOLD:
            if batch:
                translated_chunks.append(translator.ro_en.translate(" ".join(batch)))
                batch = []
                batch_length = 0

            for i in range(0, len(sentence), TRANSLATOR_THRESHOLD):
                chunk = sentence[i:i + TRANSLATOR_THRESHOLD]
                translated_chunks.append(translator.ro_en.translate(chunk))

        else:
            new_length = batch_length + len(sentence) + (1 if batch else 0)

            if new_length > TRANSLATOR_THRESHOLD:
                translated_chunks.append(translator.ro_en.translate(" ".join(batch)))
                batch = [sentence]
                batch_length = len(sentence)
            else:
                batch.append(sentence)
                batch_length = new_length

    if batch:
        translated_chunks.append(translator.ro_en.translate(" ".join(batch)))

    return " ".join(translated_chunks)


def get_text_from_image(path, translator):
    text = extract_text(path)
    return translate_text(text, translator)
