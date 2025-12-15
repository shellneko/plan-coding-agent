from plan_coding_agent.functions.go2 import *
from plan_coding_agent.functions.navigation import *
from plan_coding_agent.functions.audio import *
from plan_coding_agent.functions.agent import *

def main():
    speak("今日はいい天気だなあ。", "普通")
    walk(1.0, 30)
    speak("どこに行こうかな。", "普通")
    walk(1.0, -45)
    speak("なんだか楽しい気分だ。", "普通")
    walk(1.0, 0)
    speak("ぶらぶら歩くのも悪くないな。", "普通")
    walk(1.0, 15)

if __name__ == "__main__":
    main()
