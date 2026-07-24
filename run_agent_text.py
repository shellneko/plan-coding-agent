from plan_coding_agent.agent_chain import agent_chain
from plan_coding_agent.utils import play_mp3


while True:
    text = input("> ")
    print(f"[INFO] ユーザー入力: {text}")

    play_mp3("./sounds/start_transcribe.mp3")

    print("[INFO] エージェントによる行動計画を開始します")
    result = agent_chain(text)
    print("[DEBUG] スクリプト実行結果：")
    print(result)

    play_mp3("./sounds/play_finish.mp3")
