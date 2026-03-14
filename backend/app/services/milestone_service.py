from fastapi import APIRouter, Body
from app.services.session_manager import get_session

router = APIRouter()

@router.get("/milestone/{session_id}")
def milestone(session_id: str):
    s = get_session(session_id) or {}
    msgs = s.get("messages", 0)
    if msgs >= 15: level = 3
    elif msgs >= 5: level = 2
    elif msgs >=1: level = 1
    else: level = 0
    return {"level": level, "messages": msgs}