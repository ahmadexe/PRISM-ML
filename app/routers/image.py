from fastapi import APIRouter
from ..services.image import analyze_nsfw_image
from ..services.image import analyze_gore_image
from ..services.image import analyze_offensive_image
from ..services.image import analyze_text_image


router = APIRouter()

@router.get("/mod/image/nsfw", tags=["image"])
async def nsfw():
    return await analyze_nsfw_image()

@router.get("/mod/image/gore", tags=["image"])
async def gore():
    return await analyze_gore_image()

@router.get("/mod/image/offensive", tags=["image"])
async def offensive():
    return await analyze_offensive_image()

@router.get("/mod/image/text", tags=["image"])
async def text():
    return await analyze_text_image()
