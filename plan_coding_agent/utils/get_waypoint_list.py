import yaml
from pathlib import Path


def get_waypoint_list():
    waypoints_file = Path("waypoints.yaml")
    waypoints_file.touch(exist_ok=True)

    with open(waypoints_file, "r") as f:
        waypoints = yaml.safe_load(f)

    if waypoints is None:
        return []

    return list(waypoints.keys())
