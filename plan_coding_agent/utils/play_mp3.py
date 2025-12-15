from pydub import AudioSegment
from pydub.playback import play


def play_mp3(file_name):
    sound = AudioSegment.from_mp3(file_name)
    play(sound)
