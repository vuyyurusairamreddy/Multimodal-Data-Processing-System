from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text):
    if not text or len(text.strip()) == 0:
        return None
    
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.astype(np.float32)

def compute_similarity(query_embedding, doc_embeddings):
    similarities = []
    
    for doc_emb in doc_embeddings:
        if doc_emb is not None:
            similarity = np.dot(query_embedding, doc_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb)
            )
            similarities.append(similarity)
        else:
            similarities.append(0.0)
    
    return similarities

def find_relevant_documents(query, documents, top_k=3):
    query_embedding = generate_embedding(query)
    
    if query_embedding is None:
        return []
    
    doc_embeddings = [doc['embedding'] for doc in documents]
    similarities = compute_similarity(query_embedding, doc_embeddings)
    
    doc_similarity_pairs = list(zip(documents, similarities))
    doc_similarity_pairs.sort(key=lambda x: x[1], reverse=True)
    
    top_documents = [doc for doc, sim in doc_similarity_pairs[:top_k] if sim > 0.3]
    
    return top_documents
