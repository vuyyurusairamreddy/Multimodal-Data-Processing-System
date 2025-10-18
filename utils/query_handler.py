# query handler placeholder
import requests
from config import PERPLEXITY_API_KEY, PERPLEXITY_MODEL, PERPLEXITY_API_URL

def query_perplexity(user_query, context_documents):
    context_text = "\n\n".join([
        f"Document: {doc['filename']}\nContent: {doc['content'][:1000]}"
        for doc in context_documents
    ])
    
    system_prompt = f"""You are an AI assistant with access to a knowledge base containing multimodal documents. 
Use the following context to answer the user's question accurately and comprehensively.

Context from knowledge base:
{context_text}

If the context does not contain relevant information, use your general knowledge but indicate that the information is not from the uploaded documents."""
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": PERPLEXITY_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    }
    
    try:
        response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        answer = result['choices'][0]['message']['content']
        
        return answer
    
    except Exception as e:
        return f"Error querying Perplexity API: {str(e)}"
