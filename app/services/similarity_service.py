import numpy as np
import tensorflow_hub as hub
from app.models.similarity_result import SimilarityResult

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
print("module %s loaded" % module_url)

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def calculate_similarity(resume_text, job_description_texts):
    results = []
    query_vec = model([resume_text])[0]
    for job_description_text in job_description_texts:
        file_vec = model([job_description_text])[0]
        similarity_score = 1 - cosine(query_vec, file_vec)
        results.append(SimilarityResult(job_description=job_description_text, similarity_score=similarity_score))
    return results