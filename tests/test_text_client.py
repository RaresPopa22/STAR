import os.path

import pytest

from src.text_client import get_text_from_image
from src.translator_client import TranslatorClient


def test_img_text_extraction():
    test_file_path = "1.jpeg"
    assert os.path.exists(test_file_path)

    test_translator = TranslatorClient()
    text = get_text_from_image(test_file_path, test_translator.ro_en)

    assert "NaHCO3" in text
    assert "TDS" in text
    assert "New York" in text
    assert "GH/KH" in text
    assert "Barista" in text
