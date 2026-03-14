from fastapi import APIRouter, Body
from app.services.image_service import generate_couple_image

router = APIRouter()

@router.post("/generate-image")
def gen_image(body: dict = Body(...)):
    # body: {session_id, user_image_url, wife_avatar_url, style}
    out_url = generate_couple_image(body["user_image_url"], body["wife_avatar_url"])
    return {"image_url": out_url}