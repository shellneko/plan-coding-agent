import os

import requests
from langchain_core.messages.human import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from .openai_tts import tts
from .play_audio import play_audio

SERVER_URL = "http://100.99.242.83:8000"


def nav(waypoint_name: str):
    print(f"nav({waypoint_name})")


def speak(text: str, style="親しく"):
    print(f"speak({text}, {style})")
    # tts(text=text, style=style)
    # play_audio("tts.mp3")
    # os.remove("tts.wav")


def walk(x: float, yaw: float):
    payload = {
        "x": x,
        "yaw": yaw,
    }
    requests.post(f"{SERVER_URL}/api/go2/move", json=payload)


def damp():
    requests.post(f"{SERVER_URL}/api/go2/damp")


def sit():
    requests.post(f"{SERVER_URL}/api/go2/sit")


def stand_up():
    requests.post(f"{SERVER_URL}/api/go2/stand_up")


def wave_hand():
    requests.post(f"{SERVER_URL}/api/go2/hello")


def draw_heart():
    requests.post(f"{SERVER_URL}/api/go2/heart")


def stretch():
    requests.post(f"{SERVER_URL}/api/go2/stretch")


def dance():
    requests.post(f"{SERVER_URL}/api/go2/dance")


def analyze_camera():
    response = requests.get(f"{SERVER_URL}/api/go2/get_image")
    data = response.json()
    img = data["image"]
    message = HumanMessage(
        content=[
            {"type": "text", "text": "この画像を簡潔に説明してください"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img}"},
            },
        ]
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    res = llm.invoke([message])
    return res.content


class QueryOutput(BaseModel):
    is_match: bool = Field(description="画像の内容とクエリーが一致しているかどうか")


def query_camera(query: str):
    response = requests.get(f"{SERVER_URL}/api/go2/get_image")
    data = response.json()
    img = data["image"]
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": f"この画像の内容とクエリーが一致しているか確認してください。\nquery: {query}",
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img}"},
            },
        ]
    )

    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
    ).with_structured_output(QueryOutput)
    res = model.invoke([message])
    return res.is_match
