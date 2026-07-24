from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class QueryTextOutput(BaseModel):
    is_match: bool = Field(
        description="入力テキストの内容とクエリーが一致しているかどうか"
    )

def query_text(text: str, query: str):
    llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0).with_structured_output(
        QueryTextOutput
    )
    res = llm.invoke(
        f"入力テキストの内容とクエリーの意味的な内容が一致しているか判定してください：\n・入力テキスト: {text}\n・クエリー: {query}"
    )
    return res.is_match


def call_llm(query: str):
    llm = ChatOpenAI(model="gpt-5.5", temperature=0, reasoning_effort="none")
    res = llm.invoke(query)
    return res.content
