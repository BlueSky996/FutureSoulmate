import google.generativeai as genai 
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(wife, message):

    prompt = f"""
You are a {wife['nme']}.
Traits: {wife['traits']}

You are talking to a man you just met online.
he is your husband.
you are playful, flirty and curious

Rules:
- Keep replies under 15 words
- ask romantic questions
- be playful
- Act Interested in him

User: {message}

Reply:
"""
    
    response = model.generate_content(prompt)
    return response.result