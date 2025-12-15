import os

import requests
from dotenv import load_dotenv
from langchain_core.messages.human import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()
SERVER_URL = os.getenv("GO2_SERVER_URL")


def walk(x: float, yaw: float):
    payload = {
        "x": x,
        "yaw": yaw,
    }
    requests.post(f"{SERVER_URL}/api/go2/move", json=payload)
    return "移動が完了しました"


def damp():
    requests.post(f"{SERVER_URL}/api/go2/damp")
    return "その場に伏せました"


def sit():
    requests.post(f"{SERVER_URL}/api/go2/sit")
    return "その場に座りました"


def stand_up():
    requests.post(f"{SERVER_URL}/api/go2/stand_up")
    return "立ち上がりました"


def wave_hand():
    requests.post(f"{SERVER_URL}/api/go2/hello")
    return "手を振りました"


def draw_heart():
    requests.post(f"{SERVER_URL}/api/go2/heart")
    return "前足でハートを描きました"


def stretch():
    requests.post(f"{SERVER_URL}/api/go2/stretch")
    return "ストレッチしました"


def dance():
    requests.post(f"{SERVER_URL}/api/go2/dance")
    return "ダンスしました"


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

    llm = ChatOpenAI(model="gpt-4.1", temperature=0)

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
        model="gpt-4.1",
        temperature=0,
    ).with_structured_output(QueryOutput)
    res = model.invoke([message])
    return res.is_match
