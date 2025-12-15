import os

from .execute_code import execute_code
from .extract_python_block import extract_python_block
from .get_waypoint_list import get_waypoint_list
from .openai_tts import openai_tts
from .play_mp3 import play_mp3
from .realtime_api import RealtimeAPI


def tts(text: str, style: str, voice: str):
    openai_tts(text=text, style=style, voice=voice, file_name="tts.mp3")
    play_mp3("tts.mp3")
    os.remove("tts.mp3")


def stt(timeout_sec=10):
    realtime = RealtimeAPI(api_key=os.getenv("OPENAI_API_KEY"))
    transcription, timeout = realtime.transcribe(timeout_sec=timeout_sec)
    if timeout:
        return None
    return transcription
