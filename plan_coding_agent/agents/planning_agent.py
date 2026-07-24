from langchain_openai import ChatOpenAI
from plan_coding_agent.prompts.planning import prompt_template


def planning_agent(user_input: str):
    prompt = prompt_template.invoke({"user_input": user_input})
    llm = ChatOpenAI(model="gpt-5.5", reasoning_effort="none", temperature=0)
    res = llm.invoke(prompt)
    return res.content
