# agent/reasoning.py
import os
from dotenv import load_dotenv
from app.utils_cleaner import clean_text

load_dotenv()

GEMINI_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_KEY:
    raise RuntimeError("GOOGLE_API_KEY missing")

import google.generativeai as genai
genai.configure(api_key=GEMINI_KEY)

MODEL_NAME = "models/gemini-1.0-pro"


class ReasoningEngine:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)

    async def chat(self, prompt: str) -> str:
        try:
            res = self.model.generate_content(prompt)
            return clean_text(res.text)
        except Exception as e:
            return f"[Gemini error] {e}"

    async def reason(self, prompt: str) -> str:
        try:
            res = self.model.generate_content(
                "Think step by step and answer clearly:\n\n" + prompt
            )
            return clean_text(res.text)
        except Exception as e:
            return f"[Gemini error] {e}"
