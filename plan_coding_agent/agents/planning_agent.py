from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from plan_coding_agent.prompts.planning import prompt_template


def planning_agent(user_input: str):
    prompt = prompt_template.invoke({"user_input": user_input})
    #llm = ChatOpenAI(model="gpt-4.1", temperature=0)
    llm = ChatOllama(model="qwen3.6:35b", temperature=0.5, base_url="http://100.68.33.14:11434", reasoning=False)
    res = llm.invoke(prompt)
    return res.content
