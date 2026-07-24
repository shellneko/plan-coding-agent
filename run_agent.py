from plan_coding_agent.agent_chain import agent_chain
from plan_coding_agent.utils import play_mp3, stt

from plan_coding_agent.utils.wakeword import WakeWord

wwd = WakeWord()

while True:
    print("[INFO] ウェイクワード待機中...")
    wwd.wait()

    print("[INFO] ウェイクワードを検出しました")
    print("[INFO] ユーザー音声入力を開始します")
    play_mp3("./sounds/start_transcribe.mp3")

    text = stt(timeout_sec=10)
    if text is None:
        print("[ERROR] 音声入力がタイムアウトしました")
        play_mp3("./sounds/timeout_transcribe.mp3")
        continue
    print(f"[INFO] ユーザー入力: {text}")

    print("[INFO] エージェントによる行動計画を開始します")
    result = agent_chain(text)
    print("[DEBUG] スクリプト実行結果：")
    print(result)

    play_mp3("./sounds/play_finish.mp3")
