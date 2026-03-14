import google.generativeai as genai 
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(message):

    prompt = f"""
You are a romantic AI wife.
Reply lovingly and playfully.

User: {message}
"""
    
    response = model.generate_content(prompt)
    return response.result