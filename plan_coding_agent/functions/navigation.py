import os

import requests
import yaml
from dotenv import load_dotenv

load_dotenv()
SERVER_URL = os.getenv("NAV_SERVER_URL")


def nav(target_waypoint: str):
    with open("waypoints.yaml", "r") as f:
        waypoints = yaml.safe_load(f)
        if waypoints is None:
            # return "ウェイポイントが一つも登録されていません"
            return False

    if target_waypoint not in waypoints:
        # return "指定したウェイポイントが登録されていません"
        return False

    response = requests.post(
        f"{SERVER_URL}/api/nav/send_goal", json=waypoints[target_waypoint]
    )
    data = response.json()
    # return data["result"]
    if data["result"] == "ナビゲーションに成功しました":
        return True
    return False


def set_waypoint(waypoint_name: str):
    with open("waypoints.yaml", "r") as f:
        waypoints = yaml.safe_load(f)
        if waypoints is None:
            waypoints = {}

    response = requests.get(f"{SERVER_URL}/api/nav/get_current_pose")
    data = response.json()
    # print(data)

    waypoints[waypoint_name] = data
    with open("waypoints.yaml", "w") as f:
        yaml.safe_dump(waypoints, f, allow_unicode=True)

    # return "登録が完了しました。"
    return True


def delete_waypoint(waypoint_name: str):
    with open("waypoints.yaml", "r") as f:
        waypoints = yaml.safe_load(f)
        if waypoints is None:
            # return "ウェイポイントが一つも登録されていません"
            return False

    if waypoint_name not in waypoints:
        # return "そのウェイポイントはウェイポイント一覧に登録されていません"
        return False

    waypoints.pop(waypoint_name)

    with open("waypoints.yaml", "w") as f:
        yaml.safe_dump(waypoints, f, allow_unicode=True)

    # return "削除が完了しました"
    return True


def get_waypoint_list():
    with open("waypoints.yaml", "r") as f:
        waypoints = yaml.safe_load(f)

    if waypoints is None:
        return str([])

    return str(list(waypoints.keys()))
