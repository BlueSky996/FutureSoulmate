from fastapi import APIRouter, Body
from google import genai
import os,random

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

religon = [
    'christian',
    'muslim',
    'jew',
    'hindu',
    'catholic'
]

def generate_wife_image(wife):
    prompt = f"""
    Beautiful woman named {wife['name']}, age {wife['age']},
    traits: {', '.join(wife['traits'])},
    religon: {wife['religon']}
    realistic portrait, soft lighting, high quality, selfie, teasing
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt
    )
    return "/images/wife1.jpg"



@router.post("/generate-wife")
def generate_wife(req: dict = Body(...)):

    user_traits = req.get("traits")
    user_name = req.get("name")

    wife = {
        "name": user_name or random.choice(names),
        "age": random.randint(20,35),
        "traits": user_traits if user_traits else random.sample(traits,2),
    }

    # generate image after character is created
    image_url = generate_wife_image(wife) # gemini call
    wife ["image"] = image_url

    return wife
