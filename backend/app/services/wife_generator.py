from fastapi import APIRouter
import random

router = APIRouter()

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

@router.post("/generate-wife")
def generate_wife():

    wife = {
        "name": random.choice(names),
        "age": random.randint(20,35),
        "traits": random.sample(traits,2),
        "image": "/images/wife1.jpg"
    }

    return wife
