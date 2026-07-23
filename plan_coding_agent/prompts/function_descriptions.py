from plan_coding_agent.utils import get_waypoint_list

waypoints = get_waypoint_list()

function_descriptions = f"""\
1. query_camera(query: str) -> bool:
    カメラの内容とクエリの内容が一致していたらTrue, そうでなければFalseを返す。

2. walk(x: float, yaw: float):
    yaw(度)回転した後、x(m)直進する。yawは正で左回り、負で右回り。xは正で前進、負で後退。

3. draw_heart():
    手でハートを描く。

4. stretch():
    ストレッチする。

5. dance():
    ダンスする。

6. wave_hand():
    手を振る。

7. damp():
    伏せる。

8. sit():
    座る。

9. stand_up:
    立ち上がる。

10. speak(text: str, style: str):
    textの内容をstyleで指定した喋り方の音声に変換してスピーカーで再生する（例： speak("こんにちは", "元気よく")）。

11. transcribe() -> Optional[str]:
    マイクに入力された音声をテキストに変換する。もし10秒間何も入力されなかったらNoneを返す。

12. query_text(text: str, query: str) -> bool:
    textの内容とqueryの内容が一致していたらTrueを返す。そうでなければFalseを返す。

13. nav(target_waypoint: str) -> bool:
    指定したウェイポイントに自律ナビゲーションする。ナビゲーションに成功したらTrue、失敗したらFalseを返す。

14. set_waypoint(waypoint_name: str):
    指定した名前で、現在地点をウェイポイントとして追加する。

15. delete_waypoint(waypoint_name) -> bool:
    指定したウェイポイントを削除する。ウェイポイントが一つも登録されていない、または指定したウェイポイントが存在しない場合はFalse、削除に成功したらTrueを返す。

16. get_waypoint_list() -> str:
    現在のウェイポイントのリストを取得する。戻り値は文字列である（例：　ウェイポイントがない場合は"[]", ある場合は"['A', 'B', 'C']"という感じ）。

17. call_llm(query: str) -> str:
    queryをLLMに入力し、その出力を得る

18. call_vlm(query: text) -> str:
    queryとカメラ画像をVLMに入力し、その出力を得る

19. jump():
    前方にジャンプする
"""
