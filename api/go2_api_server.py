import base64
import math
import time
from typing import Dict
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

import uvicorn
from fastapi import FastAPI

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import (
    ObstaclesAvoidClient,
)
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.go2.video.video_client import VideoClient


load_dotenv()
nic = str(os.getenv("NIC"))

ChannelFactoryInitialize(0, nic)
app = FastAPI()

sport_client = SportClient()
sport_client.SetTimeout(10.0)
sport_client.Init()

avoid_client = ObstaclesAvoidClient()
avoid_client.SetTimeout(3.0)
avoid_client.Init()
while not avoid_client.SwitchGet()[1]:
    avoid_client.SwitchSet(True)
    time.sleep(0.1)
avoid_client.UseRemoteCommandFromApi(True)

video_client = VideoClient()
video_client.SetTimeout(3.0)
video_client.Init()


@app.post("/api/go2/move")
def move(payload: Dict):
    x = payload["x"]
    yaw = payload["yaw"]

    vx = 1 if x >= 0 else -1
    vyaw = 1 if yaw >= 0 else -1

    avoid_client.Move(0, 0, vyaw)
    time.sleep(abs(math.radians(yaw)))

    avoid_client.Move(vx, 0, 0)
    time.sleep(abs(x))

    avoid_client.Move(0, 0, 0)

    return {"success": True}


@app.post("/api/go2/euler")
def euler(payload: Dict):
    sport_client.Euler(
        float(payload["roll"]), float(payload["pitch"]), float(payload["yaw"])
    )
    return {"success": True}


@app.post("/api/go2/damp")
def damp():
    sport_client.Damp()
    time.sleep(2)
    return {"success": True}


@app.post("/api/go2/sit")
def sit():
    sport_client.Sit()
    time.sleep(1)
    return {"success": True}


@app.post("/api/go2/stand_up")
def stand_up():
    sport_client.RecoveryStand()
    time.sleep(2)
    return {"success": True}


@app.post("/api/go2/heart")
def heart():
    sport_client.Heart()
    time.sleep(1)
    return {"success": True}


@app.post("/api/go2/hello")
def hello():
    sport_client.Hello()
    time.sleep(1)
    return {"success": True}


@app.post("/api/go2/stretch")
def stretch():
    sport_client.Stretch()
    time.sleep(1)
    return {"success": True}


@app.post("/api/go2/dance")
def dance():
    sport_client.Dance1()
    time.sleep(7)
    return {"success": True}


@app.get("/api/go2/get_image")
def get_image():
    code, data = video_client.GetImageSample()
    if code != 0:
        return {"success": False, "image": None}

    img_b64 = base64.b64encode(bytes(data)).decode("utf-8")
    return {"success": True, "image": img_b64}

@app.get("/api/go2/get_image_bytes")
def get_image():
    code, data = video_client.GetImageSample()
    if code != 0:
        return {"success": False, "image": None}

    return {"success": True, "image": bytes(data)}


if __name__ == "__main__":
    parsed_url = urlparse(os.getenv("GO2_SERVER_URL"))
    uvicorn.run(app, host="0.0.0.0", port=parsed_url.port)