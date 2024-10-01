from fastapi import APIRouter
from typing import List
from app.models.similarity_result import SimilarityResult
from app.services.similarity_service import calculate_similarity

router = APIRouter()

@router.post("/job-match/", tags=["job-match"])
async def job_match(resume_text: str, job_description_texts: List[str]):
    results = calculate_similarity(resume_text, job_description_texts)
    return {"results": results}
