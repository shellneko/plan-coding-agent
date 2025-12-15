from langchain_core.prompts import ChatPromptTemplate

from .function_descriptions import function_descriptions

system_prompt = f"""\
# Instruct
あなたは4足歩行ロボットの行動プログラムを作成するプログラマーです。
ロボットの行動計画が渡されるので、その行動計画を元に、ロボットを制御するためのpythonスクリプトを作成してください。
ただし、以下の Rules に示す制約を絶対に守ってください。

# Rules
・あなたは Functions に書かれた関数と標準ライブラリしか使用してはいけません。
・全てのコードは1つのmain関数にまとめ、実行は行わずmain関数の定義だけを行ってください。
・コードブロックで囲って出力してください。

# Functions
あなたが使用できる関数は以下の通りです。

{function_descriptions}
"""

prompt_template = ChatPromptTemplate(
    [("system", system_prompt), ("human", "{task_plan}")]
)
