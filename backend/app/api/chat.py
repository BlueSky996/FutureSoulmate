from fastapi import APIRouter
from app.services.gemini_service import ask_gemini

router = APIRouter()

@router.post("/chat")
async def chat(message: str):

    reply = ask_gemini(message)

    return {"reply": reply}