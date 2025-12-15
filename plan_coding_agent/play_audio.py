import asyncio

from aiortc.contrib.media import MediaPlayer
from unitree_webrtc_connect.webrtc_driver import (
    UnitreeWebRTCConnection,
    WebRTCConnectionMethod,
)


async def async_play(file_name: str):
    # Choose a connection method (uncomment the correct one)
    # conn = UnitreeWebRTCConnection(WebRTCConnectionMethod.LocalSTA, ip="192.168.8.181")
    conn = UnitreeWebRTCConnection(
        WebRTCConnectionMethod.LocalSTA, serialNumber="B42D4000NC58G80X"
    )
    # conn = UnitreeWebRTCConnection(WebRTCConnectionMethod.Remote, serialNumber="B42D2000XXXXXXXX", username="email@gmail.com", password="pass")
    # conn = UnitreeWebRTCConnection(WebRTCConnectionMethod.LocalAP)

    await conn.connect()

    player = MediaPlayer(file_name)  # Use MediaPlayer for MP3
    audio_track = player.audio  # Get the audio track from the player
    conn.pc.addTrack(audio_track)  # Add the audio track to the WebRTC connection

    await asyncio.sleep(3600)  # Keep the program running to handle events


def play_audio(file_name: str):
    asyncio.run(async_play(file_name))
