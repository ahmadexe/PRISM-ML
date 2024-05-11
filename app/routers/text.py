from fastapi import APIRouter
from ..services.text import analyze_text
from ..models.text import Text


router = APIRouter()

@router.get("/mod/text", tags=["text"])
async def text(text: Text):
    return await analyze_text(text)
