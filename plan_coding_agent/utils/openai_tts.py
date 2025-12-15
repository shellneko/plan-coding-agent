from openai import OpenAI


def openai_tts(text: str, style: str, voice="coral", file_name="tts.mp3"):
    client = OpenAI()

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
        instructions=style,
    ) as response:
        response.stream_to_file(file_name)
