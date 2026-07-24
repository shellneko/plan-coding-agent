from fastapi import FastAPI
import uvicorn
import threading
from pydantic import BaseModel
from urllib.parse import urlparse
import os

import rclpy
from rclpy.executors import MultiThreadedExecutor
from nav2_node import Nav2APINode


app = FastAPI()
rclpy.init()

nav2_node = Nav2APINode()
executor = MultiThreadedExecutor(num_threads=2)
executor.add_node(nav2_node)
nav2_thread = threading.Thread(target=executor.spin, daemon=True)
nav2_thread.start()


class Pose(BaseModel):
    x: float
    y: float
    z: float
    qx: float
    qy: float
    qz: float
    qw: float

@app.post("/api/nav/send_goal")
async def send_goal(goal_pose: Pose):
    success, message = await nav2_node.send_goal(pose=goal_pose.model_dump())
    return {"success": success, "message": message}

# get current pose from map -> base_link
@app.get("/api/nav/get_current_pose")
def get_current_pose():
    current_pose = nav2_node.get_current_pose()
    if current_pose is None:
        return {"success": False, "message": "現在位置の取得に失敗しました"}
    
    return {"success": True, "pose": current_pose}


if __name__ == "__main__":
    parsed_url = urlparse(os.getenv("NAV2_SERVER_URL"))
    uvicorn.run(app, host="0.0.0.0", port=parsed_url.port)