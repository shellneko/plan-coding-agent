import os
import subprocess

TEMPLATE = """\
from plan_coding_agent.functions.go2 import *
from plan_coding_agent.functions.navigation import *
from plan_coding_agent.functions.audio import *
from plan_coding_agent.functions.agent import *

{{main}}

if __name__ == "__main__":
    main()
"""


def execute_code(code: str):
    python_code = TEMPLATE.replace("{{main}}", code)
    with open("tmp.py", "w") as f:
        f.write(python_code)

    result = subprocess.run(
        ["python", "tmp.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    # os.remove("tmp.py")

    return result.stdout
