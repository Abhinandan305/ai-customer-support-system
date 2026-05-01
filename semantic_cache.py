from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SemanticCache:
    def __init__(self, threshold=0.85):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.threshold = threshold

        self.index = faiss.IndexFlatIP(384)  # cosine similarity (normalized vectors)
        self.questions = []
        self.answers = []

    def _embed(self, text):
        vec = self.model.encode([text])
        vec = vec / np.linalg.norm(vec)  # normalize for cosine similarity
        return vec.astype("float32")

    def get(self, query):
        if len(self.questions) == 0:
            return None

        query_vec = self._embed(query)

        scores, idx = self.index.search(query_vec, 1)

        # similarity score
        score = scores[0][0]

        if score > self.threshold:
            answer = self.answers[idx[0][0]]

            # safety check
            if answer is None:
                return None

            return answer

        return None

    def set(self, query, answer):
        # prevent caching empty responses
        if not answer or answer == "None":
            return

        vec = self._embed(query)

        self.index.add(vec)
        self.questions.append(query)
        self.answers.append(answer)