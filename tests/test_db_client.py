from unittest.mock import MagicMock

from src.db_client import save, query_db, create_collection


def test_save():
    mock_config = {'text_splitter': {'chunk_size': 1000, 'chunk_overlap': 200}}
    mock_collection = MagicMock()
    text = "Text to save"
    chunks = save(mock_config, mock_collection,"mock.jpg", text)

    mock_collection.add.assert_called_once()
    call_kwargs = mock_collection.add.call_args.kwargs
    assert 'ids' in call_kwargs
    assert 'documents' in call_kwargs
    assert [text] == chunks


def test_save_long_text():
    mock_config = {'text_splitter': {'chunk_size': 1000, 'chunk_overlap': 200}}
    mock_collection = MagicMock()
    sentence = "A very long sentence "
    n = 1000 // len(sentence) + 1
    long_sentence = sentence * n + "."

    chunks = save(mock_config, mock_collection, "mock.jpg", long_sentence)
    call_kwargs = mock_collection.add.call_args.kwargs
    assert len(chunks) > 1
    assert len(call_kwargs['documents']) > 1


def test_query():
    mock_collection = MagicMock()
    expected_result = {'documents': [['result']], 'ids': [[1]]}
    mock_collection.query.return_value = expected_result

    query_text = 'this is a query'
    result = query_db(mock_collection, query_text)

    assert result == expected_result
    mock_collection.query.assert_called_with(query_texts=query_text, n_results=1)


def test_create_collection():
    mock_config = {}
    mock_client = MagicMock()
    mock_ef = MagicMock()

    create_collection(mock_config, client=mock_client, ef=mock_ef)
    mock_client.get_or_create_collection.assert_called_once_with(name="documents", embedding_function=mock_ef)
