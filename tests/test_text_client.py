import os.path
import pytest

from src.text_client import extract_text, translate_text, _get_text_from_image
from src.translator_client import TranslatorClient
from unittest.mock import Mock, patch, MagicMock


@pytest.mark.integration
def test_img_text_extraction():
    test_file_path = "1.jpeg"
    assert os.path.exists(test_file_path)

    text = extract_text(test_file_path)

    assert "ACTE" in text
    assert "H.G. nr. 430" in text
    assert "01/05/2008 - original" in text


@pytest.mark.integration
def test_scan_pdf_text_extraction():
    test_file_path = "2.pdf"
    assert os.path.exists(test_file_path)

    text = extract_text(test_file_path)
    print(text)

    assert "TSH" in text
    assert "06.10.2025 - 09:07" in text
    assert "0.161 μUI/mL" in text


@pytest.mark.integration
def test_pdf_text_extraction():
    test_file_path = "3.pdf"
    assert os.path.exists(test_file_path)

    text = extract_text(test_file_path)
    print(text)

    assert "MONTH 20XX" in text
    assert "123 YOUR STREET" in text


@pytest.mark.integration
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


@pytest.mark.unit
def test_translate_text_over_threshold():
    mock_config = {
        "translator": {"threshold": 4999}
    }
    n = 5000
    long_sentence = "a" * n

    mock_translator = Mock()
    mock_translator.translate.side_effect = lambda x: x

    translated_text = translate_text(mock_config, long_sentence, mock_translator)

    assert mock_translator.translate.call_count == 2

    for call_args in mock_translator.translate.call_args_list:
        chunk = call_args[0][0]
        assert len(chunk) <= 4999


@pytest.mark.unit
@patch('src.text_client.get_ocr')
def test_img_text_extraction_unit(mock_get_ocr):
    mock_ocr = MagicMock()
    mock_ocr.predict.return_value = [{"rec_texts": ["Line 1", "Line 2"]}]
    mock_get_ocr.return_value = mock_ocr

    mock_file = "mock.jpg"
    result = _get_text_from_image(mock_file)

    assert result == "Line 1\nLine 2"
    mock_ocr.predict.assert_called_once_with(input=mock_file)


@pytest.mark.unit
@patch('src.text_client.get_nlp')
def test_translate_text_unit(mock_get_nlp):
    mock_config = {"translator": {"threshold": 5000}}
    mock_doc = MagicMock()
    mock_sent = MagicMock()
    mock_sentence = "Propozitie test"
    mock_sent.text = mock_sentence
    mock_doc.sents = [mock_sent]

    mock_nlp = MagicMock(return_value=mock_doc)
    mock_get_nlp.return_value = mock_nlp

    mock_translator = Mock()
    expected = "Test sentence"
    mock_translator.translate.return_value = expected

    result = translate_text(mock_config, mock_sentence, mock_translator)

    assert result == expected
    mock_translator.translate.assert_called_once()
