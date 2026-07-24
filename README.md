# Plan Coding Agent

Unitree Go2を、OpenAIを利用したAIエージェントから音声またはテキストで操作するためのプロジェクトです。Go2の基本動作、カメラ画像の確認、登録済みウェイポイントへのナビゲーションなどを自然言語で指示できます。

各コマンドは、特に記載がない限りリポジトリのルートディレクトリで実行してください。

## インストール

事前に、以下のコマンドを利用できるようにしてください。

- Git
- CMake
- uv
- C/C++のビルド環境

次のスクリプトを実行してインストールします。

```bash
./install.sh
```

`install.sh`はCyclone DDSを取得してビルドした後、そのインストール先を`CYCLONEDDS_HOME`に設定して`uv sync`を実行します。

音声機能を使用する環境では、PyAudioが利用するPortAudioと、pydubが音声を再生するために利用するffmpegが別途必要になる場合があります。

## 環境変数

リポジトリのルートディレクトリに`.env`を作成し、利用する環境に合わせて設定してください。

```dotenv
OPENAI_API_KEY=your-openai-api-key
GO2_SERVER_URL=http://127.0.0.1:8000
NAV_SERVER_URL=http://127.0.0.1:8001
NAV2_SERVER_URL=http://127.0.0.1:8001
NIC=your-network-interface
```

各変数の用途は次のとおりです。

- `OPENAI_API_KEY`: AIエージェント、音声認識、画像認識で利用するOpenAI APIキーです。
- `GO2_SERVER_URL`: AIエージェントがGo2制御APIへ接続するためのURLです。
- `NAV_SERVER_URL`: AIエージェントと`helper/`のナビゲーション用ツールがNavigation2 APIへ接続するためのURLです。
- `NAV2_SERVER_URL`: Navigation2 APIサーバーが待ち受けるポートを決めるためのURLです。通常は`NAV_SERVER_URL`と同じURLを設定します。
- `NIC`: Go2と通信するネットワークインターフェース名です。例としてLinuxでは`eth0`、macOSでは`en0`などがあります。実際にGo2へ接続しているインターフェースを指定してください。

`.env`にはAPIキーなどの秘密情報が含まれるため、Gitへコミットしないでください。

`go2_api_server.py`は`.env`を直接読み込みます。一方、`nav2_api_server.py`を起動するときは`NAV2_SERVER_URL`がプロセスの環境変数として参照できる必要があります。`.env`を利用する場合は、次のように起動できます。

```bash
uv run --env-file .env api/nav2_api_server.py
```

## AIエージェントの実行

### 音声で指示する

```bash
uv run run_agent.py
```

ウェイクワードを検出すると音声入力を開始し、認識した指示に基づいてAIエージェントが行動計画を作成して実行します。マイクとスピーカーが利用できる環境が必要です。

### テキストで指示する

```bash
uv run run_agent_text.py
```

プロンプトに自然言語の指示を入力すると、AIエージェントが行動計画を作成して実行します。

## Go2制御APIサーバー

Go2と通信できるネットワークに接続し、`.env`の`NIC`と`GO2_SERVER_URL`を設定してから、次のコマンドを実行します。

```bash
uv run api/go2_api_server.py
```

Go2を制御するFastAPIサーバーが起動します。このサーバーは、移動、姿勢変更、起立・着座、ジェスチャー、ダンス、カメラ画像取得などのAPIを提供します。

## ナビゲーションAPIサーバー

ナビゲーション機能を利用するには、あらかじめROS 2とNavigation2によるナビゲーションシステムが構築され、以下が利用可能になっている必要があります。

- Navigation2の`/navigate_to_pose`アクション
- `map`フレームから`base_link`フレームへのTF
- 地図、自己位置推定、経路計画、Go2の移動制御

Navigation2システムを起動したうえで、次のコマンドを実行します。

```bash
uv run api/nav2_api_server.py
```

これにより、現在位置の取得と目的地の送信を行うFastAPIサーバーが起動します。`.env`から環境変数を渡す場合は、前述の`uv run --env-file .env api/nav2_api_server.py`を使用してください。

ROS 2のパッケージは`uv`ではインストールされません。`rclpy`、`nav2_msgs`、`geometry_msgs`、`tf2_ros`などを利用できるROS 2環境で実行してください。

## helper

`helper/`には、セットアップやナビゲーションを補助する次のスクリプトがあります。

### `download_wakeword_models.py`

openWakeWordが提供する学習済みウェイクワードモデルをダウンロードします。

```bash
uv run helper/download_wakeword_models.py
```

### `set_waypoint.py`

Navigation2から取得したGo2の現在位置を、指定した名前のウェイポイントとして`waypoints.yaml`へ保存します。

```bash
uv run helper/set_waypoint.py <ウェイポイント名>
```

例:

```bash
uv run helper/set_waypoint.py entrance
```

実行前にNavigation2 APIサーバーを起動し、`.env`の`NAV_SERVER_URL`を設定してください。

### `nav_waypoint.py`

`waypoints.yaml`に登録されたウェイポイントをNavigation2へ送信し、Go2のナビゲーションを開始します。

```bash
uv run helper/nav_waypoint.py <ウェイポイント名>
```

例:

```bash
uv run helper/nav_waypoint.py entrance
```

実行前にNavigation2 APIサーバーを起動し、`.env`の`NAV_SERVER_URL`を設定してください。
