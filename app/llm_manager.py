"""
llm_manager.py
Correct Gemini wrapper (2025-compatible)
Uses GenerativeModel + generate_content
"""

import os
from app.utils_cleaner import clean_text
import google.generativeai as genai

GEMINI_KEY = os.getenv("GOOGLE_API_KEY")
STANDARD_MODEL = os.getenv("GEMINI_STANDARD_MODEL", "gemini-1.5-flash")
REASONING_MODEL = os.getenv("GEMINI_REASON_MODEL", "gemini-1.5-pro")

if not GEMINI_KEY:
    raise RuntimeError("❌ GOOGLE_API_KEY not set")

genai.configure(api_key=GEMINI_KEY)

# Load models once
standard_model = genai.GenerativeModel(STANDARD_MODEL)
reasoning_model = genai.GenerativeModel(REASONING_MODEL)


async def ask_gemini_standard(prompt: str) -> str:
    try:
        response = standard_model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"[Gemini standard error] {e}"


async def ask_gemini_reasoning(prompt: str) -> str:
    try:
        response = reasoning_model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"[Gemini reasoning error] {e}"


async def ask_gemini(prompt: str, reasoning: bool = False) -> str:
    if reasoning:
        return await ask_gemini_reasoning(prompt)
    return await ask_gemini_standard(prompt)
