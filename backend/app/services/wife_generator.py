import random

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

def generate_wife():

    return {
        "name": random.choice(names),
        "traits": random.sample(traits, 2),
        "age": random.randint(20, 35)
    }
