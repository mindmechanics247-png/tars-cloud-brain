"""
config.py
Loads all environment variables for TARS Cloud Brain.
Supports:
- Gemini (chat + reasoning)
- Google Search API
- OpenWeather API
- LiveKit API
- SerpAPI (RAG)
- N8N MCP webhook
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
# 🤖 GEMINI API (main + reasoning)
# ---------------------------------------------------------
GEMINI_KEY = os.getenv("GOOGLE_API_KEY", "")

GEMINI_STANDARD_MODEL = os.getenv(
    "GEMINI_STANDARD_MODEL",
    "gemini-1.5-flash"
)

GEMINI_REASON_MODEL = os.getenv(
    "GEMINI_REASON_MODEL",
    "gemini-2.0-flash-thinking"
)

# ---------------------------------------------------------
# 🔎 GOOGLE SEARCH API (Sachdeva style)
# ---------------------------------------------------------
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY", "")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID", "")

# ---------------------------------------------------------
# 🌦 WEATHER API (OpenWeather)
# ---------------------------------------------------------
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# ---------------------------------------------------------
# 🔍 SERP API (optional)
# ---------------------------------------------------------
SERP_KEY = os.getenv("SERPAPI_KEY", "")

# ---------------------------------------------------------
# 🎤 LIVEKIT (optional)
# ---------------------------------------------------------
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "")

# ---------------------------------------------------------
# 🧿 YOLO Vision
# ---------------------------------------------------------
YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "models/yolov8n.pt")

# ---------------------------------------------------------
# 🧠 MEMORY & GENERAL CONFIG
# ---------------------------------------------------------
PASSWORD = os.getenv("PASSWORD", "ANANT_TARS_123")
MAX_MEMORY = int(os.getenv("MAX_MEMORY_ITEMS", "500"))
PORT = int(os.getenv("PORT", "8000"))

# ---------------------------------------------------------
# 🔄 N8N MCP Webhook
# ---------------------------------------------------------
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")

# ---------------------------------------------------------
# 🚫 Local LLM disabled
# ---------------------------------------------------------
LOCAL_LLM_ENABLED = os.getenv("LOCAL_LLM_ENABLED", "false").lower() in ("1", "true", "yes")

# ---------------------------------------------------------
# Debug print
# ---------------------------------------------------------
print("\n--- TARS CONFIG LOADED ---")
print("Gemini Key:", "SET" if GEMINI_KEY else "NOT SET")
print("Google Search Key:", "SET" if GOOGLE_SEARCH_API_KEY else "NOT SET")
print("Weather Key:", "SET" if OPENWEATHER_API_KEY else "NOT SET")
print("SerpAPI:", "SET" if SERP_KEY else "NOT SET")
print("LiveKit:", "SET" if LIVEKIT_API_KEY else "NOT SET")
print("N8N Webhook:", "SET" if N8N_WEBHOOK_URL else "NOT SET")
print("YOLO Model:", YOLO_MODEL_PATH)
print("Local LLM Enabled:", LOCAL_LLM_ENABLED)
print("------------------------------------------\n")
