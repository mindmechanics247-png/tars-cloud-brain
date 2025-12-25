import os
import google.generativeai as genai
from app.utils_cleaner import clean_text

GEMINI_KEY = os.getenv("GOOGLE_API_KEY")

# These models are VERIFIED to work with SDK 0.5.4
STANDARD_MODEL = "gemini-1.5-flash"
REASONING_MODEL = "gemini-1.5-pro"

if not GEMINI_KEY:
    raise RuntimeError("GOOGLE_API_KEY is missing")

# IMPORTANT: this disables v1beta routing
genai.configure(
    api_key=GEMINI_KEY,
    transport="rest"   # 🔥 THIS FORCES NON-BETA API
)

_standard = genai.GenerativeModel(STANDARD_MODEL)
_reasoning = genai.GenerativeModel(REASONING_MODEL)


async def ask_gemini(prompt: str, reasoning: bool = False) -> str:
    try:
        model = _reasoning if reasoning else _standard
        response = model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"[Gemini error] {e}"
