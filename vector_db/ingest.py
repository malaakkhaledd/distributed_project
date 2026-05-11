from vector_db.store import add_document

documents = [
    "Distributed systems use multiple machines to process tasks.",
    "Load balancing distributes requests across workers.",
    "Workers execute tasks in parallel for efficiency.",
    "Vector databases store embeddings for similarity search."
]

def load_documents():
    for doc in documents:
        add_document(doc)