from unittest.mock import Mock, patch
from src.llm_client import ask_assistant


def test_ask_assistant():
    mock_config = {"relevance_threshold": 1}
    mock_translator = Mock()
    translated_query = "query"
    mock_translator.translate.return_value = translated_query

    mock_collection = Mock()
    context = "context"
    mock_collection.query.return_value = {'documents': [[context]], 'distances': [['0.1']]}

    with patch('src.llm_client.ollama.chat') as mock_ollama:
        expected_answer = 'answer'
        mock_ollama.return_value = {'message': {'content': expected_answer}}

        original_query = "interogare"
        res = ask_assistant(mock_config, mock_collection, mock_translator, original_query)
        mock_translator.translate.assert_called_once_with(original_query)
        mock_collection.query.assert_called_once_with(query_texts=translated_query, n_results=5)
        call_args = mock_ollama.call_args
        print(f"call_args={call_args}")
        prompt = call_args.kwargs['messages'][0]['content']

        assert context in prompt
        assert original_query in prompt
        assert res == expected_answer
