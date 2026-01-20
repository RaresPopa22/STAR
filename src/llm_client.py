import logging

import ollama

logger = logging.getLogger(__name__)


def ask_assistant(config, collection, translator, query):
    try:
        query_en = translator.translate(query)
        results = collection.query(query_texts=query_en, n_results=5)
        documents = results['documents'][0]
        distances = results['distances'][0]

        relevance_threshold = int(config['relevance_threshold'])
        context_parts = []
        for i, (doc, dist) in enumerate(zip(documents, distances)):
            if float(dist) < relevance_threshold:
                context_parts.append(f"[Document {i + 1}\n{doc}]")

        context = "\n\n".join(context_parts) if context_parts else "No relevant context found"

        prompt = f"""
        Use the following pieces of context to answer the question at the end. 
        The context contains multiple document chunks, ranked by relevance.
        
        Strict rules:
        1. Answer ONLY based on the context.
        2. If the date formats are US (MM/DD), convert them to Romanian format (DD.MM.YYYY)
        3. If multiple documents contain relevant info, synthesize them
        
        --- CONTEXT (English) ---
        {context}
        --- END CONTEXT ---
        
        Question(Romanian): {query}
        Answer(in Romanian):"""

        response = ollama.chat(model='llama3.1', messages=[
            {'role': 'user', 'content': prompt}
        ])

        return response['message']['content']
    except Exception as e:
        logger.error(f'ask_assistant failed with {e}')
        return "Nu am putut procesa cererea. Vă rugăm încercați din nou."
