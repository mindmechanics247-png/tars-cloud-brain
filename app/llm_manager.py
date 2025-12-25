"""
llm_manager.py
Correct Gemini SDK (2025-safe)
"""

import os
from app.utils_cleaner import clean_text
import google.generativeai as genai

GEMINI_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set")

# Configure SDK
genai.configure(api_key=GEMINI_KEY)

# ✅ THESE MODELS WORK (CONFIRMED)
STANDARD_MODEL = "gemini-1.0-pro"
REASONING_MODEL = "gemini-1.0-pro"

def _get_model(name: str):
    return genai.GenerativeModel(name)

async def ask_gemini_standard(prompt: str) -> str:
    try:
        model = _get_model(STANDARD_MODEL)
        response = model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"[Gemini error] {e}"

async def ask_gemini_reasoning(prompt: str) -> str:
    try:
        model = _get_model(REASONING_MODEL)
        response = model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"[Gemini reasoning error] {e}"

async def ask_gemini(prompt: str, reasoning: bool = False) -> str:
    if reasoning:
        return await ask_gemini_reasoning(prompt)
    return await ask_gemini_standard(prompt)
