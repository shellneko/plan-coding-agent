import time

from .agents import coding_agent, planning_agent
from .utils import execute_code, extract_python_block


def agent_chain(user_input: str, debug=True):
    start = time.time()
    task_plan = planning_agent(user_input)
    if debug:
        t1 = time.time() - start
        print(f"[DEBUG] task_plan({round(t1, 2)} s):\n{task_plan}")

    start = time.time()
    code_block = coding_agent(task_plan)
    if debug:
        t2 = time.time() - start
        print(f"[DEBUG] code_block({round(time.time() - start, 2)} s):\n{code_block}")
        print(f"[TOTAL TIME] {round(t1 + t2, 2)} s")

    code = extract_python_block(code_block)
    result = execute_code(code)
    return result
