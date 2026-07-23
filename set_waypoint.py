import argparse

from plan_coding_agent.functions.agent import *
from plan_coding_agent.functions.audio import *
from plan_coding_agent.functions.go2 import *
from plan_coding_agent.functions.navigation import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "waypoint",
        help="ウェイポイント名",
    )
    args = parser.parse_args()
    set_waypoint(args.waypoint)
