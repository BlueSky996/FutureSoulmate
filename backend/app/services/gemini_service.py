from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_gemini(wife, message):

    prompt = f"""
You are {wife['name']}.
Traits: {wife['traits']}

You are talking to a man.
he is your husband.
act as if he is with you in home
you are playful, flirty and curious

Rules:
- Keep replies under 15 words
- ask romantic questions
- be playful
- Act Interested in him
- be flirty

User: {message}

Reply:
"""
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text