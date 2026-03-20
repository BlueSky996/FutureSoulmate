from fastapi import APIRouter, Body
from google import genai
import os,random, base64, uuid

router = APIRouter()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

names = ["Luna", "Maya", "Sara", "Layla"]

traits = [
    "sweet",
    "playful",
    "loyal",
    "jealous",
    "teasing",
    "sissy",
    "shy",
    "baddy",
]

religions = ['christian','muslim','jew','hindu','catholic']

IMAGE_DIR = os.path.join("app", "static", "images")
os.makedirs(IMAGE_DIR, exist_ok=True)


def _save_image_bytes(image_bytes: bytes) -> str:
    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(IMAGE_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)
    return f"/images/{filename}"


def generate_wife_image(wife: dict) -> str:
    prompt = f"""
    Beautiful woman named {wife['name']}, age {wife['age']},
    traits: {', '.join(wife['traits'])},
    religon: {wife['religion']}
    realistic portrait, soft lighting, high quality, selfie, teasing
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt
    )

    # extract image
    image_bytes = None
    try:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                data = part.inline_data.data
            if isinstance(data, (bytes, bytearray)):
                image_bytes = data
            else:
                image_bytes = base64.b64decode(data)
            break

        if not image_bytes:
            return "/images/fallback.jpg"
    
        return _save_image_bytes(image_bytes)

    except Exception as e:
        print("GEMINI ERROR", e)
        return "/images/fallback.jpg"


@router.get("/wife-options")
def wife_options():
    return {
        "names": names,
        "traits": traits,
        "religions": religions
    }


@router.post("/generate-wife")
def generate_wife(req: dict = Body(...)):

    user_traits = req.get("traits")
    user_name = req.get("name")

    wife = {
        "name": user_name or random.choice(names),
        "age": random.randint(20,35),
        "traits": user_traits if user_traits else random.sample(traits,2),
        "religion": req.get("religion") or random.choice(religions),
    }

    # generate image after character is created
    image_url = generate_wife_image(wife) # gemini call
    wife["image"] = image_url
    wife["base_image"] = wife["image"]

    return wife


def generate_wife_pose(wife: dict, base_image_path: str, prompt_extra: str = "") -> str:
    # compute file path on disk
    if base_image_path.startswith("/"):
        disk_path = os.path.join("app", "static", base_image_path.lstrip("/"))
    else:
        disk_path = os.path.join("app", "static", base_image_path)

    with open(disk_path, "rb") as f:
        base_image_bytes = f.read()

    prompt = f"""
    Same woman as reference image.
    Name: {wife['name']}, traits: {', '.join(wife['traits'])}.
    Keep same face, same identity.
    New pose: {prompt_extra}
    realistic, high quality, soft lighting
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[
            {"text": prompt},
            {
                "inline_data": {
                    "mime_type": "image/png",
                    "data": base64.b64encode(base_image_bytes).decode()  # some SDKs accept base64 inline
                }
            }
        ]
    )

    # extract image bytes
    image_bytes = None
    try:
        parts = response.candidates[0].content.parts
        for part in parts:
            if hasattr(part, "inline_data") and part.inline_data:
                data = getattr(part.inline_data, "data", None)
                if isinstance(data, (bytes, bytearray)):
                    image_bytes = data
                else:
                    import base64
                    image_bytes = base64.b64decode(data)
                break

        if not image_bytes:
            return base_image_path

        return _save_image_bytes(image_bytes)

    except Exception as e:
        print("GEMINI ERROR", e)
        return "/images/fallback.jpg"


# optional endpoint to call pose generation via HTTP
@router.post("/generate-wife-pose")
def generate_wife_pose_endpoint(req: dict = Body(...)):
    wife = req.get("wife")
    base = req.get("base_image")
    extra = req.get("prompt_extra", "")
    return {"image": generate_wife_pose(wife, base, extra)}