import os
import time

from plan_coding_agent.utils import stt, tts

"""
from plan_coding_agent.utils.realtime_api import RealtimeAPI
def speak(text: str):
    print(f"speak({text})")
    start = time.time()
    realtime = RealtimeAPI(api_key=os.getenv("OPENAI_API_KEY"))
    realtime.play(text, voice="alloy")
    print(f"[DEBUG] {round(time.time() - start, 2)} s")
"""

def speak(text: str, style: str = "普通に喋ってください"):
    print(f"speak({text}, {style})")
    start = time.time()
    tts(text=text, style=style, voice="coral")
    print(f"[DEBUG] {round(time.time() - start, 2)} s")

def transcribe():
    text = stt(timeout_sec=10)
    return text
