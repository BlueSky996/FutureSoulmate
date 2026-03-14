from fastapi import APIRouter
from app.services.gemini_service import ask_gemini
from app.services.session_manager import get_session, create_session, increment_messages


router = APIRouter()

@router.post("/chat")
async def chat(req: dict = Body(...)):
    sid = req.get("session_id") or create_session()
    user_msg = req.get["message"]
    wife_data = req["wife"]

    reply = ask_gemini(wife_data, user_msg)
    increment_messages(sid)

    return {"reply": reply, "session_id": sid}