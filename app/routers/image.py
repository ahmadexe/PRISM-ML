from fastapi import APIRouter
from ..services.image import analyze_nsfw_image
from ..services.image import analyze_gore_image
from ..services.image import analyze_offensive_image
from ..services.image import analyze_text_image
from ..models.image import Image


router = APIRouter()

@router.get("/mod/image/nsfw", tags=["image"])
async def nsfw(image: Image):
    return await analyze_nsfw_image(image)

@router.get("/mod/image/gore", tags=["image"])
async def gore(image: Image):
    return await analyze_gore_image(image)

@router.get("/mod/image/offensive", tags=["image"])
async def offensive(image: Image):
    return await analyze_offensive_image(image)

@router.get("/mod/image/text", tags=["image"])
async def text(image: Image):
    return await analyze_text_image(image)
