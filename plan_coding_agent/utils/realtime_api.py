import asyncio
import base64
import json
import time

import pyaudio
import websockets

from .audio_io import AudioIO


class RealtimeAPI:
    def __init__(self, api_key):
        self.realtime_url = "wss://api.openai.com/v1/realtime?model=gpt-realtime"
        self.headers = {"Authorization": f"Bearer {api_key}"}

        self.timer_stop = False

        audio_config = {
            "format": pyaudio.paInt16,
            "channels": 1,
            "rate": 24000,
            "chunk": 1024,
        }
        self.aio = AudioIO(input_config=audio_config, output_config=audio_config)

    def transcribe(self, timeout_sec=5):
        return asyncio.run(self._async_transcribe(timeout_sec=timeout_sec))

    def play(self, text, voice="alloy"):
        return asyncio.run(self._async_play(text, voice))

    async def _async_transcribe(self, timeout_sec):
        self.aio.init_input()
        self.timer_stop = False

        session = await websockets.connect(
            uri=self.realtime_url, additional_headers=self.headers
        )

        await session.send(self._get_transcription_payload())

        transcription, _, timeout = await asyncio.gather(
            self._recv_transcription(session),
            self._send_audio(session),
            self._timer(session, timeout_sec),
        )

        self.aio.close_input()
        return (transcription, timeout)

    async def _async_play(self, text, voice):
        self.aio.init_output()

        session = await websockets.connect(
            uri=self.realtime_url, additional_headers=self.headers
        )
        await session.send(self._get_play_payload(voice=voice))
        await session.send(self._get_create_response_payload(text=text))
        result = await self._recv_audio(session)

        await session.close()
        self.aio.close_output()
        return result

    async def _timer(self, session, timeout_sec):
        start = time.time()
        while not self.timer_stop:
            # print(f"{time.time() - start} sec")
            if time.time() - start >= timeout_sec:
                await session.close()
                return True
            await asyncio.sleep(0)
        return False

    async def _recv_transcription(self, session):
        try:
            async for message in session:
                message = json.loads(message)
                # print(message["type"])
                if message["type"] == "input_audio_buffer.speech_started":
                    self.timer_stop = True
                elif (
                    message["type"]
                    == "conversation.item.input_audio_transcription.completed"
                ):
                    await session.close()
                    return message["transcript"]
        except Exception:
            return None

    async def _recv_audio(self, session):
        async for message in session:
            message = json.loads(message)
            # print(f"[DEBUG] {message['type']}")
            if message["type"] == "response.output_audio.delta":
                audio_delta = message["delta"]
                audio_bytes = base64.b64decode(audio_delta)
                await self.aio.async_write(audio_bytes)
            elif message["type"] == "response.output_audio.done":
                # print("[DEBUG] audio done")
                return True

    async def _send_audio(self, session):
        try:
            while True:
                audio_bytes = await self.aio.async_read()
                if audio_bytes is None:
                    continue

                audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
                await session.send(self._get_audio_append_payload(audio_b64))
        except Exception:
            return

    def _get_transcription_payload(self):
        return json.dumps(
            {
                "type": "session.update",
                "session": {
                    "type": "realtime",
                    "audio": {
                        "input": {
                            "format": {"type": "audio/pcm", "rate": 24000},
                            "turn_detection": {
                                "type": "server_vad",
                                "create_response": False,
                                "interrupt_response": False,
                                "prefix_padding_ms": 300,
                                "silence_duration_ms": 500,
                                "threshold": 0.5,
                            },
                            # far_field はラップトップ, near_field はイヤフォン向けの設定
                            # "noise_reduction": {"type": "far_field"},
                            "noise_reduction": {"type": "near_field"},
                            "transcription": {
                                "language": "ja",
                                "model": "gpt-4o-transcribe",
                            },
                        }
                    },
                },
            }
        )

    def _get_play_payload(self, voice):
        return json.dumps(
            {
                "type": "session.update",
                "session": {
                    "type": "realtime",
                    "audio": {
                        "input": {
                            "format": {"type": "audio/pcm", "rate": 24000},
                        },
                        "output": {
                            "format": {"type": "audio/pcm", "rate": 24000},
                            "voice": voice,
                        },
                    },
                    # "instructions": "Convert the text provided by the user into speech.",
                    "model": "gpt-realtime",
                },
            }
        )

    def _get_create_response_payload(self, text):
        return json.dumps(
            {
                "type": "response.create",
                "response": {
                    "instructions": "Convert the text provided by the user into speech verbatim. Do not reply in any way, just read it aloud.",
                    "conversation": "none",
                    "output_modalities": ["audio"],
                    "input": [
                        {
                            "type": "message",
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": f"Please translate the following sentences into audio:\n{text}",
                                }
                            ],
                        }
                    ],
                },
            }
        )

    def _get_audio_append_payload(self, audio_base64):
        return json.dumps(
            {
                "type": "input_audio_buffer.append",
                "audio": f"{audio_base64}",
            }
        )
