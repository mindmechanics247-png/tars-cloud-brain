"""
MCP Client
Connects TARS Agent to N8N / external tools
"""

class MCPClient:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name, handler):
        self.tools[name] = handler

    def execute(self, name, payload):
        if name not in self.tools:
            return "Tool not found."
        return self.tools[name](**payload)
