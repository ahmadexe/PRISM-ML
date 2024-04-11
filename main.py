from fastapi import FastAPI
from app.routers import text
from app.routers import image

app = FastAPI()

app.include_router(text.router)
app.include_router(image.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}