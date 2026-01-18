import uuid
import logging

import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_DATA_PATH = '../chroma_data/'
EMBEDDING_MODEL = 'paraphrase-multilingual-MiniLM-L12-v2'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_collection(client=None, ef=None):
    client = client or chromadb.PersistentClient(path=CHROMA_DATA_PATH)
    ef = ef or embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL, device='mps')
    return client.get_or_create_collection(name="documents", embedding_function=ef)


def save(collection, text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_text(text)
    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(ids=ids, documents=chunks)
    return chunks


def query_db(collection, query_text):
    return collection.query(query_texts=query_text, n_results=1)


def peek(collection):
    count = collection.count()
    logger.info(f"Total chunks in the DB: {count}")

    peek = collection.peek(5)
    for i, doc in enumerate(peek['documents']):
        logger.info(f"Chunk: {doc[:100]}")
