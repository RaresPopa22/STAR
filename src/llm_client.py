import ollama


def ask_assistant(collection, translator, query):
    query_en = translator.translate(query)
    results = collection.query(query_texts=query_en, n_results=1)
    context = results['documents'][0][0]

    prompt = f"""
    Use the following pieces of context to answer the question at the end. 
    Use the following CONTEXT (which is translated from Romanian)
    
    Strict rules:
    1. Answer ONLY based on the context.
    2. If the date formats are US (MM/DD), convert them to Romanian format (DD.MM.YYYY)
    
    --- CONTEXT (English) ---
    {context}
    --- END CONTEXT ---
    
    Question(Romanian): {query}
    Answer(in Romanian):"""

    response = ollama.chat(model='llama3.1', messages=[
        {'role': 'user', 'content': prompt}
    ])

    return response['message']['content']
