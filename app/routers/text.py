from fastapi import APIRouter
from ..services.text import analyze_text


router = APIRouter()

@router.post("/text", tags=["text"])
async def text():
    return await analyze_text()
