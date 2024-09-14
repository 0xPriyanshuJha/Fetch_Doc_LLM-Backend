import faiss
import numpy as np
from app.db import fetch_documents


#Faiss index
index = faiss.IndexFlatL2(512)

def search_documents(text: str, top_k: int, threshold: float):
    """
    Search for the documents based on the query text by the user.
    Params:
    text: The query text entered by the user
    top_k: The number of top results to return
    threshold: The minimum similarity score to consider for the search

    Returns:
    query_embedding: The embedding of the query text
    indices: The indices of the documents in the index
    documents: The list of documents based on the indices
    """
    query_embedding = embed_text(text)
    _, indices = index.search(np.array([query_embedding]), top_k)

    # fetch the documents based on the indices
    documents = fetch_documents(indices)
    return[
        doc for doc in documents
        if cosine_similarity(doc['embedding'], query_embedding) >= threshold  # filter based on the threshold
    ]

# function to calculate cosine similarity
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

# function to embed the text
def embed_text(text):
    return np.random.random(512)