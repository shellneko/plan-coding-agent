from plan_coding_agent.functions.go2 import *
from plan_coding_agent.functions.navigation import *
from plan_coding_agent.functions.audio import *
from plan_coding_agent.functions.agent import *

def main():
    used_words = []
    while True:
        # 1. ユーザーの発話をテキスト化
        user_word = transcribe()
        # 2. Noneの場合は再度促す
        if user_word is None:
            speak("何も聞こえませんでした。もう一度お願いします。", "普通")
            continue
        # 3. 取得した単語をリストに追加
        used_words.append(user_word)
        # 4. generate_textで次の単語を生成
        used_words_str = "[" + ", ".join(used_words) + "]"
        query = f"しりとりで「{user_word}」の次の単語。ただしすでに{used_words_str}は使われている。"
        next_word = generate_text(query)
        # 5. speakで生成した単語を発話
        speak(next_word, "普通")
        # 6. 使われた単語リストに生成した単語を追加
        used_words.append(next_word)
        # 7. 生成した単語の最後が「ん」で終わっていないか判定
        if query_text(next_word[-1], "ん"):
            speak("「ん」で終わったので私の負けです。", "普通")
            break
        # 8. 以降、1に戻り繰り返す

if __name__ == "__main__":
    main()
