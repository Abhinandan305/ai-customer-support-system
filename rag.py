import json
import os
from sentence_transformers import SentenceTransformer

# ---------------------------
# Load policies safely
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICY_PATH = os.path.join(BASE_DIR, "policies.json")

with open(POLICY_PATH, "r", encoding="utf-8") as f:
    policies = json.load(f)

# ---------------------------
# Convert JSON → Documents
# ---------------------------
documents = []

for category, items in policies.items():
    for item in items:
        documents.append(
            f"[{category.upper()}] {item['title']}: {item['content']}"
        )

# ---------------------------
# Embedding model
# ---------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(documents, show_progress_bar=True)

# ---------------------------
# Retrieval function
# ---------------------------
def retrieve_context(query, top_k=3):
    query_embedding = model.encode([query])

    # cosine similarity
    import numpy as np

    scores = np.dot(embeddings, query_embedding.T).flatten()

    top_indices = scores.argsort()[-top_k:][::-1]

    results = [documents[i] for i in top_indices]

    return "\n\n".join(results)