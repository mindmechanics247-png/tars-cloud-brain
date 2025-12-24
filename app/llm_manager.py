"""
llm_manager.py
Gemini wrapper (STANDARD + REASONING)
Compatible with latest google-generativeai SDK
"""

import os
from app.config import GEMINI_KEY
from app.utils_cleaner import clean_text

# Safe import
GEMINI_AVAILABLE = False
try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_KEY)
    GEMINI_AVAILABLE = True
except Exception as e:
    GEMINI_AVAILABLE = False

STANDARD_MODEL = os.getenv("GEMINI_STANDARD_MODEL", "gemini-1.5-flash")
REASONING_MODEL = os.getenv("GEMINI_REASON_MODEL", "gemini-2.0-flash-thinking")


async def _ask(model_name: str, prompt: str, max_tokens: int) -> str:
    if not GEMINI_AVAILABLE:
        return "[Gemini unavailable] Check GOOGLE_API_KEY"

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": 0.6,
            },
        )

        if hasattr(response, "text"):
            return clean_text(response.text)

        return clean_text(str(response))

    except Exception as e:
        return f"[Gemini error] {e}"


async def ask_gemini_standard(prompt: str, max_tokens: int = 512) -> str:
    """Fast / short response"""
    return await _ask(STANDARD_MODEL, prompt, max_tokens)


async def ask_gemini_reasoning(prompt: str, max_tokens: int = 1024) -> str:
    """Deep reasoning response"""
    return await _ask(REASONING_MODEL, prompt, max_tokens)


async def ask_gemini(prompt: str, reasoning: bool = False) -> str:
    if reasoning:
        return await ask_gemini_reasoning(prompt)
    return await ask_gemini_standard(prompt)
