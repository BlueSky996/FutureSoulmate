from fastapi import APIRouter, Body
from app.services.gemini_service import ask_gemini
from app.services.session_manager import get_session, create_session, increment_messages
from app.services.soulmate_generator import generate_soulmate_pose

router = APIRouter()

OFFER_LINK = "https://www.google.com"

@router.post("/chat")
async def chat(req: dict = Body(...)):

    sid = req.get("session_id") or create_session()
    user_msg = req.get("message", "")
    soulmate_data = req["soulmate"]

    if not soulmate_data:
        return {"error": "soulmate data missing", "status": 400}

    session = get_session(sid)

    if "base_image" not in session:
        session["base_image"] = soulmate_data["image"]
    # add flags to prevent repeat
    if "image_sent" not in session:
        session["image_sent"] = False

    increment_messages(sid)
    messages = session["messages"]

    # LEVEL 1
    if messages == 3 and not session["image_sent"]:
        session["image_sent"] = True
        return {
            "type": "image",
            "image": "/images/soulmate1.jpg",
            "text": "I just took this for you ❤️",
            "session_id": sid
        }
    
    # OFFER 
    if messages == 4 and not session["image_sent"]:
        session["offer_sent"] = True
        return {
            "type": "offer",
            "text": "Come join me here and let's talk more! my subscription is about to end ",
            "link": OFFER_LINK,
            "session_id": sid
        }
    
    if messages > 4 and messages % 20 == 0:
        new_img = generate_soulmate_pose(
            soulmate_data,
            session["base_image"],
            prompt_extra="sending a teasing selfie"
        )

        return {
            "type": "image",
            "image": new_img,
            "text": "Missed me?",
            "session_id": sid
        }
    
    # Normal chat
    reply = ask_gemini(soulmate_data, user_msg)

    return {
            "type": "chat", 
            "text": reply,
            "session_id": sid
            }