TOOLS = {
    "search_web": {
        "description": "Search the web for factual or recent information using SERP API. Use for news, scores, or live facts.",
        "params": {"query": "string"}
    },
    "get_weather": {
        "description": "Get current weather for a city using OpenWeather or similar service.",
        "params": {"city": "string"}
    },
    "vision_detect": {
        "description": "Analyze camera image for objects, hands, or text. Returns structured list and preview.",
        "params": {"image": "bytes/jpg"}
    },
    "run_robot_cmd": {
        "description": "Send a safe robot command to the ESP32 robot. Examples: HEAD_LEFT, HEAD_RIGHT, WAVE, FOLLOW.",
        "params": {"cmd": "string", "args": "dict"}
    }
}
