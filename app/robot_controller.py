"""
robot_controller.py
A safe robot command queue. Robot devices should poll /robot/next or connect via WS to receive commands.
This module ONLY queues commands; it does not execute OS-level actions.
"""

from typing import List, Dict
from collections import deque

QUEUE: deque = deque(maxlen=1000)

def enqueue_command(cmd: str, args: Dict = None):
    args = args or {}
    QUEUE.append({"cmd": cmd, "args": args})
    return {"queued": True, "queue_len": len(QUEUE)}

def get_next_command():
    if QUEUE:
        return QUEUE.popleft()
    return {"cmd":"NOOP"}
