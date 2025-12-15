import yaml


def get_waypoint_list():
    with open("waypoints.yaml", "r") as f:
        waypoints = yaml.safe_load(f)

    if waypoints is None:
        return []

    return list(waypoints.keys())
