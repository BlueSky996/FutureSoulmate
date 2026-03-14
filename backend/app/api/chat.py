from fastapi import APIRouter
from app.services.gemini_service import ask_gemini
from app.services.session_manager import get_session, create_session, increment_messages

router = APIRouter()

OFFER_LINK = "https://www.google.com"

@router.post("/chat")
async def chat(req: dict = Body(...)):
    sid = req.get("session_id") or create_session()
    user_msg = req.get["message"]
    wife_data = req["wife"]

    reply = ask_gemini(wife_data, user_msg)
    increment_messages(sid)

    messages = session["messages"]

    # LEVEL 1
    if messages == 3:
        return {
            "type": "image",
            "image": "/images/wife1.jps",
            "text": "I just took this for you ❤️ Do you like me?"
        }
    
    # OFFER 
    if messages == 4 :
        return {
            "type": "offer",
            "text": "Come join me privately here babe ❤️",
            "link": OFFER_LINK
        }
    
    # Normal chat
    reply = ask_gemini(wife_data, user_msg)

    return {"reply": "chat", 
            "text": reply}