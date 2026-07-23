from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from plan_coding_agent.prompts.coding import prompt_template


def coding_agent(task_plan: str):
    prompt = prompt_template.invoke({"task_plan": task_plan})
    llm = ChatOpenAI(model="gpt-5.5", reasoning_effort="none", temperature=0)
    #llm = ChatOllama(model="qwen3.6:35b", temperature=0.5, base_url="http://100.68.33.14:11434", reasoning=False)
    res = llm.invoke(prompt)
    return res.content
