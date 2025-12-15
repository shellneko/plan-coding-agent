import asyncio

import pyaudio


class AudioIO:
    def __init__(self, input_config=None, output_config=None):
        self.input_config = input_config
        self.output_config = output_config

        self.p = None
        self.input_stream = None
        self.output_stream = None

    def init(self):
        self.init_input()
        self.init_output()

    def close(self):
        self.close_input()
        self.close_output()

    def init_input(self):
        # input_config が渡されていなかったらinputの初期化処理はスキップ
        if self.input_config is None:
            return
        if self.input_stream is not None:
            return

        if self.p is None:
            self.p = pyaudio.PyAudio()

        self.input_stream = self.p.open(
            format=self.input_config["format"],
            channels=self.input_config["channels"],
            rate=self.input_config["rate"],
            input=True,
            frames_per_buffer=self.input_config["chunk"],
        )

    def init_output(self):
        # output_config が渡されていなかったらoutputの初期化処理はスキップ
        if self.output_config is None:
            return
        if self.output_stream is not None:
            return

        if self.p is None:
            self.p = pyaudio.PyAudio()

        self.output_stream = self.p.open(
            format=self.output_config["format"],
            channels=self.output_config["channels"],
            rate=self.output_config["rate"],
            output=True,
            frames_per_buffer=self.output_config["chunk"],
        )

    def close_input(self):
        # input_stream が作られていなかったらスキップ
        if self.input_stream is None:
            return

        if self.input_stream.is_active():
            self.input_stream.stop_stream()

        self.input_stream.close()
        self.input_stream = None

        if self.p is not None:
            self.p.terminate()
            self.p = None

    def close_output(self):
        # output_stream が作られていなかったらスキップ
        if self.output_stream is None:
            return

        if self.output_stream.is_active():
            self.output_stream.stop_stream()

        self.output_stream.close()
        self.output_stream = None

        if self.p is not None:
            self.p.terminate()
            self.p = None

    def read(self):
        if self.input_stream is None:
            return None

        try:
            data = self.input_stream.read(
                self.input_config["chunk"], exception_on_overflow=False
            )
        except Exception:
            data = None

        return data

    async def async_read(self):
        return await asyncio.to_thread(self.read)

    def write(self, data):
        if self.output_stream is None:
            return False

        try:
            self.output_stream.write(data)
        except Exception:
            return False

        return True

    async def async_write(self, data):
        return await asyncio.to_thread(self.write, data)
