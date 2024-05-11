from pydantic import BaseModel

class SimilarityResult(BaseModel):
    job_description: str
    similarity_score: float
