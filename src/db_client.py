import uuid
import logging
from datetime import datetime

import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_collection(config, client=None, ef=None):
    client = client or chromadb.PersistentClient(path=config['chroma_data']['path'])
    ef = ef or embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=config['sentence_transformer']['embedding_model'], device='mps')
    return client.get_or_create_collection(name="documents", embedding_function=ef)


def save(collection, filename, text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_text(text)
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadata = [{"filename": filename, "upload_date": datetime.now().isoformat(), "chunk_index": i} for i in range(len(chunks))]

    collection.add(ids=ids, metadatas=metadata, documents=chunks)
    return chunks


def query_db(collection, query_text):
    return collection.query(query_texts=query_text, n_results=1)
