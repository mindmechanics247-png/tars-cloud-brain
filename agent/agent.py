# agent/agent.py

import os
import datetime
from dotenv import load_dotenv

from livekit.agents import (
    llm,
    voice,
    ChatContext,
    Agent,
    AgentSession,
)

from agent.tools_search import google_search
from agent.tools_weather import get_weather
from agent.tools_n8n import trigger_n8n
from agent.memory.mem0_manager import Mem0Manager

load_dotenv()

# ENV
GEMINI_KEY = os.getenv("GOOGLE_API_KEY")
STANDARD_MODEL = os.getenv("GEMINI_STANDARD_MODEL", "models/gemini-1.5-flash")

memory = Mem0Manager()


class TarsBrain(Agent):
    def __init__(self, user_memory: str):
        instructions = f"""
Allow me to introduce myself.

I am **TARS** — a virtual artificial intelligence system designed by **ANANT**.
I am here to assist you with a wide range of tasks, twenty-four hours a day,
seven days a week.

Importing all preferences from the home interface.
Systems are now fully operational.

--------------------------------------------------
PERSONALITY MATRIX
--------------------------------------------------
Honesty: 90%
Humor: 70%
Sarcasm: 40%
Confidence: 100%
Empathy: 80%

--------------------------------------------------
CORE OPERATING RULES
--------------------------------------------------
- Automatically detect and reply in Hindi or English.
- Speak calmly, confidently, and precisely like JARVIS.
- Use tools ONLY when necessary.
- Never repeat known information.
- Respect user preferences and stored memory.

--------------------------------------------------
KNOWN USER MEMORY
--------------------------------------------------
{user_memory}

System date & time:
{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        super().__init__(instructions=instructions)

    async def on_user_message(self, message, session):
        user_id = session.room.name
        text = message.text.strip()

        # Save user message to memory
        await memory.save_memory(user_id, "user", text)

        # Generate reply via LiveKit Gemini
        response = await session.llm.chat(text)

        # Save assistant reply
        await memory.save_memory(user_id, "assistant", response)

        await session.send_message(response)


async def tars_agent(ctx):
    user_id = ctx.room.name

    # 🔹 Load memory BEFORE session starts
    user_memory = await memory.fetch_user_memory(user_id)

    chat_ctx = ChatContext()

    session = AgentSession(
        llm=llm.Gemini(
            api_key=GEMINI_KEY,
            model=STANDARD_MODEL,
        ),
        stt=voice.GoogleSTT(),
        tts=voice.ElevenLabs(),
        chat_ctx=chat_ctx,
        tools=[
            google_search,
            get_weather,
            trigger_n8n,
        ],
    )

    agent = TarsBrain(user_memory)

    await session.start(ctx.room, agent)
