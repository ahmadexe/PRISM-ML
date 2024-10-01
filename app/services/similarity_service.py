import numpy as np
import os
import tensorflow_hub as hub
import tensorflow as tf
from app.models.similarity_result import SimilarityResult

import warnings
import logging

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Optional: Disable oneDNN optimizations
tf.config.experimental.set_memory_growth


os.environ["TFHUB_CACHE_DIR"] = "C:/cache-tensorflow"

# Ensure the module URL is correct
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)

print(f"Module {module_url} loaded")

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def calculate_similarity(resume_text, job_description_texts):
    results = []

    # Ensure the input texts are processed within a TensorFlow session context
    resume_embedding = model([resume_text])
    query_vec = tf.squeeze(resume_embedding).numpy()  # Convert tensor to numpy array

    for job_description_text in job_description_texts:
        job_embedding = model([job_description_text])
        file_vec = tf.squeeze(job_embedding).numpy()  # Convert tensor to numpy array

        similarity_score = cosine(query_vec, file_vec)
        results.append(SimilarityResult(job_description=job_description_text, similarity_score=similarity_score))

    return results