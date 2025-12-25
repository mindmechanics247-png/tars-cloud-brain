# agent/reasoning.py
"""
reasoning.py
Stable Gemini reasoning wrapper (2025-safe)

- chat(prompt)   → fast response
- reason(prompt) → step-by-step reasoning
"""

import os
from typing import Optional
from dotenv import load_dotenv

from app.utils_cleaner import clean_text

load_dotenv()

# 🔑 API KEY (ONLY from .env)
GEMINI_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set")

# ✅ Correct Gemini SDK
import google.generativeai as genai
genai.configure(api_key=GEMINI_KEY)

# ✅ STABLE MODELS (DO NOT CHANGE)
STANDARD_MODEL = "gemini-1.0-pro"
REASONING_MODEL = "gemini-1.0-pro"


class ReasoningEngine:
    def __init__(
        self,
        standard_model: Optional[str] = None,
        reason_model: Optional[str] = None,
    ):
        self.standard_model = standard_model or STANDARD_MODEL
        self.reason_model = reason_model or REASONING_MODEL

        self.standard_llm = genai.GenerativeModel(self.standard_model)
        self.reason_llm = genai.GenerativeModel(self.reason_model)

    async def chat(self, prompt: str) -> str:
        """
        Fast, normal response
        """
        try:
            response = self.standard_llm.generate_content(prompt)
            return clean_text(response.text)
        except Exception as e:
            return f"[Gemini chat error] {e}"

    async def reason(self, prompt: str) -> str:
        """
        Step-by-step reasoning response
        """
        reasoning_prompt = (
            "You are TARS reasoning engine.\n"
            "Think step-by-step.\n"
            "Give a short plan and final answer.\n\n"
            f"User: {prompt}"
        )

        try:
            response = self.reason_llm.generate_content(reasoning_prompt)
            return clean_text(response.text)
        except Exception as e:
            return f"[Gemini reasoning error] {e}"
