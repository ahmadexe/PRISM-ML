from fastapi import APIRouter, HTTPException
from ..services.chatbot import custom_chatbot
from ..models.chatbot import ChatRequest

# Define the router
router = APIRouter()

@router.post("/chat", tags=["chat"])
async def chat(chat_request: ChatRequest):
    try:
        # Extract question from the request model
        user_input = chat_request.question
        # Call your chatbot service with user input
        response = custom_chatbot(user_input)
        # Return the chatbot's response as a JSON object
        return {"answer": response}
    except Exception as e:
        # Raise HTTP exception with the error message if something goes wrong
        raise HTTPException(status_code=500, detail=str(e))

