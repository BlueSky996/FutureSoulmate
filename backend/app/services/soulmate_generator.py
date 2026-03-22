from fastapi import APIRouter, Body
from google import genai
import os,random, base64, uuid

router = APIRouter()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

male_names = ["Liam", "Noah", "Ethan", "Zayn"]
female_names = ["Luna", "Maya", "Sara", "Layla"]

traits = [
    "sweet","playful","loyal","jealous","teasing",
    "shy","confident","romantic","dominant","soft"
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


def generate_soulmate_image(soulmate: dict) -> str:
    prompt = f"""
    Beautiful woman named {soulmate['name']}, age {soulmate['age']},
    traits: {', '.join(soulmate['traits'])},
    religon: {soulmate['religion']}
    realistic portrait, soft lighting, high quality, selfie,
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
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


@router.get("/soulmate-options")
def soulmate_options():
    return {
        "male_names": male_names,
        "female_names": female_names,
        "traits": traits,
        "religions": religions,
        "genders": ["males", "female"]
    }


@router.post("/generate-soulmate")
def generate_soulmate(req: dict = Body(...)):

    gender = req.get("gender", "female")
    if gender == "male":
       name = req.get("name") or random.choice(male_names)
    else:
       name = req.get("name") or random.choice(male_names)
            

    soulmate = {
        "name": name,
        "gender": gender,
        "age": random.randint(20,35),
        "traits": req.get("traits") or random.sample(traits,2),
        "religion": req.get("religion") or random.choice(religions),
    }

    # generate image after character is created
    image_url = generate_soulmate_image(soulmate) # gemini call
    soulmate["image"] = image_url
    soulmate["base_image"] = image_url

    return soulmate


def generate_soulmate_pose(soulmate: dict, base_image_path: str, prompt_extra: str = "") -> str:
    # compute file path on disk
    if base_image_path.startswith("/"):
        disk_path = os.path.join("app", "static", base_image_path.lstrip("/"))
    else:
        disk_path = os.path.join("app", "static", base_image_path)

    with open(disk_path, "rb") as f:
        base_image_bytes = f.read()

    prompt = f"""
    Name: {soulmate['gender']}, traits: {', '.join(soulmate['traits'])}.
    Keep same face, same identity.
    New pose: {prompt_extra}
    realistic, high quality, soft lighting
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
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
@router.post("/generate-soulmate-pose")
def generate_soulmate_pose_endpoint(req: dict = Body(...)):
    soulmate = req.get("soulmate")
    base = req.get("base_image")
    extra = req.get("prompt_extra", "")
    return {"image": generate_soulmate_pose(soulmate, base, extra)}