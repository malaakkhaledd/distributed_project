from vector_db.store import search

def retrieve(query, k=3):
    result = search(query)

    if not result:
        return "No context available"

    return result