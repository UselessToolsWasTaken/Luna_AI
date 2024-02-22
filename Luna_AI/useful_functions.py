from elevenlabs.client import ElevenLabs
from elevenlabs import generate, play, voices, client
import subprocess
import main

eleven = ElevenLabs(
    api_key="c58335b3d8a8421ebe971198a1068cd1"  # Defaults to ELEVEN_API_KEY
)
launched_app = [r'C:\Program Files\Island\Island\Application\Island.exe',
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Users\evryt\AppData\Local\Discord\app-1.0.9033\Discord.exe']

application_value = 0

# Telling the Time
def what_time():
    from datetime import datetime
    current_time = datetime.now()
    ai_time = current_time.strftime("%I:%M %p")
    time_sentence = f"You could just check your phone Boss... It is currently {ai_time}."
    time_audio = generate(api_key="c58335b3d8a8421ebe971198a1068cd1",
                          text=time_sentence,
                          voice=main.voice_id,
                          model="eleven_monolingual_v1"
                          )
    print(time_sentence)
    play(time_audio)


def launch_app():
    try:
        launch_sentence = "I'd be delighted to open this app for you Boss!"
        if application_value == 0:
            subprocess.Popen([launched_app[0]])
        elif application_value == 1:
            subprocess.Popen([launched_app[1]])
        elif application_value == 2:
            subprocess.Popen([launched_app[2]])
        island_audio = generate(api_key="c58335b3d8a8421ebe971198a1068cd1",
                                text=launch_sentence,
                                voice=main.voice_id,
                                model="eleven_monolingual_v1"
                                )
        print(launch_sentence)
        play(island_audio)
    except Exception as e:
        island_error = "I'm not really sure what you want me to open here boss?"
        error_audio = generate(api_key="c58335b3d8a8421ebe971198a1068cd1",
                               text=island_error,
                               voice=main.voice_id,
                               model="eleven_monolingual_v1"
                               )
        print(island_error, e)
        play(error_audio)
