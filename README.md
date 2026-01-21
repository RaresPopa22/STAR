# Personal Archive RAG Application

A Streamlit based document archive with RAG capabilities, able to digitize, translate and query Romanian documents using
Llama 3.1.

### Overview

```mermaid
flowchart TD
    subgraph Ingestion
        A[Input(img/pdf)] --> B[PaddleOCR/PyMuPDF] --> C[DeepTranslator] --> D[ChromaDB]
    end
    subgraph Query
        E[Question] --> F[ChromaDB] --> G[Llama 3.1] --> H[Streamlit UI]
    end
```

### Features

- **Document Upload**: hybrid ingestion, using PyMuPDF(for .pdf files) or PaddleOCR(for .jpg, .jpeg, .png) extracts text from documents
- **Translation**: automatically translates the documents to english for higher accuracy
- **Semantic search**: finding documents based on meaning
- **LLM Integration**: natural language responses using Ollama (Llama 3.1)

### Project structure

```
.
├── README.md
├── config
│   └── base_config.yaml
├── pytest.ini
├── requirements.in
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── db_client.py
│   ├── llm_client.py
│   ├── main.py
│   ├── text_client.py
│   └── translator_client.py
└── tests
    ├── __init__.py
    ├── test_db_client.py
    ├── test_llm_client.py
    └── test_text_client.py
```

### Requirements

- Python 3.10+
- Ollama (with Llama 3.1 model)
- Spacy Romanian model 'ro_core_news_sm'


### Installation

1. Clone the repo
    `https://github.com/RaresPopa22/STAR`
2. Install Python packages
    `pip install -r requirements.txt`
3. Download the Spacy model: ` python -m spacy download ro_core_news_sm`
4. Ensure Ollama is running locally

#### Configuration

                                                                                                                                                                                                                   
Edit config/base_config.yaml as needed:   

```
chroma_data:
  path: '../chroma_data/'

sentence_transformer:
  embedding_model: 'paraphrase-multilingual-MiniLM-L12-v2'
  device: 'mps'

translator:
  threshold: 5000

relevance_threshold: 1

text_splitter:
  chunk_size: 1000
  chunk_overlap: 200
```                                                                                                                                                                                                  

### Usage

- From the project root `streamlit run src/main.py` (it should automatically open in a new tab in your default browser; if not go to http://localhost:8501)


### Testing

- run all tests: `pytest`
- run only unit tests: `pytest -m unit`
- run only integration tests: `pytest -m integration`