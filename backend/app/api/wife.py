from fastapi import APIRouter
import random

router = APIRouter()

traits = [
    "sweet",
    "playful",
    "loyal",
    "jealous",
    "teasing",
]

def generate_traits():

    return random.sample(traits, 2)