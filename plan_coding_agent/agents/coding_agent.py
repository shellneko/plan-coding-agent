from langchain_openai import ChatOpenAI
from plan_coding_agent.prompts.coding import prompt_template


def coding_agent(task_plan: str):
    prompt = prompt_template.invoke({"task_plan": task_plan})
    llm = ChatOpenAI(model="gpt-5.5", reasoning_effort="none", temperature=0)
    res = llm.invoke(prompt)
    return res.content
