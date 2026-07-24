import numpy as np
import pyaudio
from openwakeword.model import Model
from pathlib import Path

from .audio_io import AudioIO

MODEL_PATH = Path(__file__).resolve().parent.parent / "wakeword_models" / "hey_mycroft_v0.1.onnx"

class WakeWord:
    def __init__(
        self, model_path=str(MODEL_PATH), inference_framework="onnx"
    ):
        audio_config = {
            "format": pyaudio.paInt16,
            "channels": 1,
            "rate": 16000,
            "chunk": 1280,
        }
        self.aio = AudioIO(input_config=audio_config)
        self.model_path = model_path
        self.inference_framework = inference_framework

    def wait(self, threshold=0.5):
        self.aio.init_input()

        model = Model(
            wakeword_models=[self.model_path],
            inference_framework=self.inference_framework,
        )

        while True:
            audio = np.frombuffer(self.aio.read(), dtype=np.int16)
            # print(audio)
            prediction = model.predict(audio)
            score = 0

            for mdl in prediction.keys():
                score = float(prediction[mdl])

            if score >= threshold:
                break

        self.aio.close_input()
