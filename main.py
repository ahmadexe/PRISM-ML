from fastapi import FastAPI
from app.routers import text

app = FastAPI()

app.include_router(text.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}