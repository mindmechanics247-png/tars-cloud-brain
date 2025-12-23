"""
livekit_integration.py
This is a safe skeleton showing how to wire LiveKit job handlers.
You need livekit-python SDK and a LiveKit server if you want real RTC voice.
We provide a minimal safe stub that documents how to add it.
"""

# NOTE: This file is a template. Do not run unless you have livekit SDK and server.
# pip install livekit==<version>  (only if you will use LiveKit)
try:
    from livekit import agents
    from livekit.agents import AgentServer, AgentSession, ChatContext
    LIVEKIT_AVAILABLE = True
except Exception:
    LIVEKIT_AVAILABLE = False

if LIVEKIT_AVAILABLE:
    server = AgentServer()

    @server.rtc_session()
    async def my_agent(ctx: agents.JobContext):
        """
        Example entrypoint: create AgentSession configured for STT/LLM/TTS.
        See LiveKit docs for full options.
        """
        metadata = ctx.job.metadata  # job metadata contains user info
        initial_ctx = ChatContext()
        initial_ctx.add_message(role="assistant", content="Hello from TARS LiveKit agent.")
        session = AgentSession(
            # configure stt, llm, tts, vad, turn detection...
        )
        await session.start(room=ctx.room, agent=agents.Agent(chat_ctx=initial_ctx))
