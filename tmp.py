from plan_coding_agent.functions.go2 import *
from plan_coding_agent.functions.navigation import *
from plan_coding_agent.functions.audio import *
from plan_coding_agent.functions.agent import *

def main():
    speak("風俗までご案内します。私についてきてください。", "丁寧に")
    
    waypoints = get_waypoint_list()
    
    if "風俗" in waypoints:
        speak("目的地の風俗を確認しました。これから移動します。", "丁寧に")
        success = nav("風俗")
        
        if success:
            speak("到着しました。こちらが風俗です。", "丁寧に")
        else:
            speak("申し訳ありません。風俗までの案内に失敗しました。安全のためここで停止します。", "申し訳なさそうに")
    else:
        speak("申し訳ありません。目的地の風俗が登録済みウェイポイントに見つかりません。安全のためここで停止します。", "申し訳なさそうに")

if __name__ == "__main__":
    main()
