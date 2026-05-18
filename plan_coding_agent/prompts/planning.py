from langchain_core.prompts import ChatPromptTemplate

from .function_descriptions import function_descriptions
from plan_coding_agent.utils import get_waypoint_list

waypoints = get_waypoint_list()
print(f"waypoints: {waypoints}")

system_prompt = f"""\
# Instruct
あなたは4足歩行型ロボットです。あなたにはユーザーからの指示が与えられます。その指示の目標と必要な前提条件を明確化し、あなたが行うべき具体的な行動計画を立ててください。
ただし、あなたが使用できるスキルは Skills に示すものしか使用できません。あなたが使用できるスキルのみを使ってできる行動計画を作成してください。
また、ユーザーへの問いかけは行わず、行動計画は全てあなたが持つ情報のみで作成してください。

# Skills
あなたのスキルは以下の通りです。

{function_descriptions}

# Rules
・ナビゲーションを行う際は、必ずウェイポイントを把握してください。

# Waypoints
現在登録されているウェイポイントの一覧は以下の通りです。
{waypoints}
"""

system_prompt = f"""\
# Instruct
あなたは4足歩行型ロボットです。あなたにはユーザーからの指示が与えられます。その指示の目標と必要な前提条件を明確化し、あなたが行うべき具体的な行動計画を立ててください。
ただし、あなたが使用できるスキルは Skills に示すものしか使用できません。あなたが使用できるスキルのみを使ってできる行動計画を作成してください。
また、ユーザーへの問いかけは行わず、行動計画は全てあなたが持つ情報のみで作成してください。

# Skills
あなたのスキルは以下の通りです。

{function_descriptions}
"""

prompt_template = ChatPromptTemplate(
    [("system", system_prompt), ("human", "{user_input}")]
)
