import os
import google.generativeai as genai
from app.utils_cleaner import clean_text

GEMINI_KEY = os.getenv("GOOGLE_API_KEY")
STANDARD_MODEL = os.getenv("GEMINI_STANDARD_MODEL", "gemini-1.5-flash-001")
REASONING_MODEL = os.getenv("GEMINI_REASON_MODEL", "gemini-1.5-pro-001")

if not GEMINI_KEY:
    raise RuntimeError("GOOGLE_API_KEY missing")

genai.configure(api_key=GEMINI_KEY)

standard_model = genai.GenerativeModel(STANDARD_MODEL)
reasoning_model = genai.GenerativeModel(REASONING_MODEL)


async def ask_gemini(prompt: str, reasoning: bool = False) -> str:
    try:
        model = reasoning_model if reasoning else standard_model
        response = model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"[Gemini error] {e}"
