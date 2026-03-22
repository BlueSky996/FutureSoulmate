from fastapi import APIRouter, Body
from app.services.image_service import generate_couple_image

router = APIRouter()

@router.post("/generate-image")
def gen_image(body: dict = Body(...)):
    # SAFE GETS (avoid crash)
    user_img = body.get("user_image_url")
    soulmate_img = body.get("soulmate_avatar_url")

    # VALIDATION
    if not user_img or not soulmate_img:
        return {"error": "missing images"}

    out_url = generate_couple_image(user_img, soulmate_img)

    return {"image_url": out_url}