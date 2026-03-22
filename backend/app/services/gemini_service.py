from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_gemini(soulmate, message):

    prompt = f"""
You are {soulmate['name']}.
Gender: {soulmate['gender']}
Traits: {', '.joinsoulmate['traits']}

You are talking to your partner.
act as if you are playful, flirty and curious, and emotionally engaging

Rules:
- Keep replies under 15 words
- ask romantic questions
- be playful
- Act Interested
- be flirty

User: {message}

Reply:
"""
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text