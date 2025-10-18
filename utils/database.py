# database utilities placeholder
import sqlite3
import json
import numpy as np
from datetime import datetime
from config import DATABASE_PATH

def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT,
            embedding BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            relevant_docs TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_document(filename, file_type, content, metadata, embedding):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    embedding_blob = embedding.tobytes() if embedding is not None else None
    metadata_json = json.dumps(metadata)
    
    cursor.execute('''
        INSERT INTO documents (filename, file_type, content, metadata, embedding)
        VALUES (?, ?, ?, ?, ?)
    ''', (filename, file_type, content, metadata_json, embedding_blob))
    
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return doc_id

def get_all_documents():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, filename, file_type, content, metadata, embedding FROM documents')
    rows = cursor.fetchall()
    
    documents = []
    for row in rows:
        doc = {
            'id': row[0],
            'filename': row[1],
            'file_type': row[2],
            'content': row[3],
            'metadata': json.loads(row[4]) if row[4] else {},
            'embedding': np.frombuffer(row[5], dtype=np.float32) if row[5] else None
        }
        documents.append(doc)
    
    conn.close()
    return documents

def save_query(query, response, relevant_docs):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    relevant_docs_json = json.dumps(relevant_docs)
    
    cursor.execute('''
        INSERT INTO queries (query, response, relevant_docs)
        VALUES (?, ?, ?)
    ''', (query, response, relevant_docs_json))
    
    conn.commit()
    conn.close()

def get_query_history(limit=10):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT query, response, created_at 
        FROM queries 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (limit,))
    
    history = cursor.fetchall()
    conn.close()
    
    return history
