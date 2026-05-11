import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384
index = faiss.IndexFlatL2(dimension)
document_store = []

def embed(text):
    vec = model.encode(text)
    vec = np.array(vec, dtype="float32")

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm

    return vec

def add_document(text):
    vec = embed(text)
    index.add(np.array([vec]))
    document_store.append(text)

def search(query):
    if len(document_store) == 0:
        return ""

    q_vec = embed(query)

    D, I = index.search(np.array([q_vec]), 1)

    return [{"text": document_store[int(I[0][0])]}]