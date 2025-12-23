# server.py

import asyncio
from livekit.agents import AgentServer
from agent.agent import tars_agent

server = AgentServer()

@server.agent()
async def start_agent(ctx):
    print("🔥 TARS AGENT ONLINE — JOINING LIVEKIT ROOM")
    await tars_agent(ctx)

if __name__ == "__main__":
    asyncio.run(server.run())
