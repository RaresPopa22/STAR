import os.path

from src.text_client import extract_text, translate_text
from src.translator_client import TranslatorClient
from unittest.mock import Mock, call


def test_img_text_extraction():
    test_file_path = "1.jpeg"
    assert os.path.exists(test_file_path)

    text = extract_text(test_file_path)

    assert "ACTE" in text
    assert "H.G. nr. 430" in text
    assert "01/05/2008 - original" in text


def test_scan_pdf_text_extraction():
    test_file_path = "2.pdf"
    assert os.path.exists(test_file_path)

    text = extract_text(test_file_path)
    print(text)

    assert "TSH" in text
    assert "06.10.2025 - 09:07" in text
    assert "0.161 μUI/mL" in text


def test_pdf_text_extraction():
    test_file_path = "3.pdf"
    assert os.path.exists(test_file_path)

    text = extract_text(test_file_path)
    print(text)

    assert "MONTH 20XX" in text
    assert "123 YOUR STREET" in text


def test_translate():
    mock_config = {
        "translator": {"threshold": 4999}
    }
    text = "Pacientul sufera de hipotiroidism."
    translator = TranslatorClient()
    translated_text = translate_text(mock_config, text, translator)

    assert "hypothyroidism" in translated_text

    text = "         "
    translated_text = translate_text(mock_config, text, translator)
    assert "" == translated_text


def test_translate_text_over_threshold():
    mock_config = {
        "translator": {"threshold": 4999}
    }
    n = 5000
    long_sentence = "a" * n

    mock_translator = Mock()
    mock_translator.ro_en.translate.side_effect = lambda x: x

    translated_text = translate_text(mock_config, long_sentence, mock_translator)

    assert mock_translator.ro_en.translate.call_count == 2

    for call_args in mock_translator.ro_en.translate.call_args_list:
        chunk = call_args[0][0]
        assert len(chunk) <= 4999
