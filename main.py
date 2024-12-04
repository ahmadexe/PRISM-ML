from fastapi import FastAPI
from app.routers import text
from app.routers import image
from app.routers import chatbot

app = FastAPI()

app.include_router(text.router)
app.include_router(image.router)
app.include_router(chatbot.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}