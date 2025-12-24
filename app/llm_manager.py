"""
llm_manager.py
Cloud Gemini wrapper for two-model setup:
- ask_gemini_standard: fast responses
- ask_gemini_reasoning: deep reasoning
Compatible with latest google-generativeai SDK
"""

import os
from typing import Optional
from app.config import GEMINI_KEY
from app.utils_cleaner import clean_text

# ----------------------------
# Safe Gemini import
# ----------------------------
GEMINI_AVAILABLE = False

try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_KEY)
    GEMINI_AVAILABLE = bool(GEMINI_KEY)
except Exception as e:
    GEMINI_AVAILABLE = False
    _IMPORT_ERROR = str(e)

# ----------------------------
# Models (from env)
# ----------------------------
STANDARD_MODEL = os.getenv("GEMINI_STANDARD_MODEL", "gemini-1.5-flash")
REASONING_MODEL = os.getenv("GEMINI_REASON_MODEL", "gemini-2.0-flash-thinking")


# ----------------------------
# Internal helper
# ----------------------------
def _run_gemini(model_name: str, prompt: str, max_tokens: int) -> str:
    if not GEMINI_AVAILABLE:
        return "[Gemini unavailable] GOOGLE_API_KEY missing or invalid"

    try:
        model = genai.GenerativeModel(model_name)

        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": 0.7,
            }
        )

        # New SDK returns response.text
        text = getattr(response, "text", None)

        if not text:
            return "[Gemini returned empty response]"

        return clean_text(text)

    except Exception as e:
        return f"[Gemini error] {e}"


# ----------------------------
# Public APIs
# ----------------------------
async def ask_gemini_standard(prompt: str, max_tokens: int = 512) -> str:
    """
    Fast / short answers
    """
    return _run_gemini(STANDARD_MODEL, prompt, max_tokens)


async def ask_gemini_reasoning(prompt: str, max_tokens: int = 1024) -> str:
    """
    Deep reasoning answers
    """
    return _run_gemini(REASONING_MODEL, prompt, max_tokens)


async def ask_gemini(prompt: str, reasoning: bool = False) -> str:
    """
    Auto router
    """
    if reasoning:
        return await ask_gemini_reasoning(prompt)
    return await ask_gemini_standard(prompt)
