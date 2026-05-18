from plan_coding_agent.functions.go2 import *
from plan_coding_agent.functions.navigation import *
from plan_coding_agent.functions.audio import *
from plan_coding_agent.functions.agent import *

def main():
    speak("こんにちは！何かお話ししましょうか？", "元気よく")
    while True:
        user_input = transcribe()
        if user_input is None:
            continue
        response = generate_text(query=user_input)
        speak(response, "普通")

if __name__ == "__main__":
    main()
