import random
import json
import subprocess
import random as r

from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import generate, play, voices, client

import google_callendar as gc
from config import LoadConfig as LC

api_keys = LC.api_keys
voice_id = LC.voice_ID

o_client = OpenAI(
    api_key=api_keys[0]
)

eleven = ElevenLabs(
    api_key=api_keys[1]
)


def tell_time():    # Luna will tell you the time!
    from datetime import datetime
    random_response = random.choice(LC.time_answer)
    current_time = datetime.now()
    ai_time = current_time.strftime("%H:%M")
    time_response = random_response.format(time=ai_time)
    audio = generate(api_key=api_keys[1],
                     text=time_response,
                     voice=voice_id,
                     model="eleven_monolingual_v1")
    print(time_response)
    play(audio)


def launch_app(index):  # She will also run you apps based on the index that is passed from main's voice_commands()!
    app_path = LC.app_path
    try:
        random_response = random.choice(LC.app_response)
        audio = generate(api_key=api_keys[1],
                         text=random_response,
                         voice=voice_id,
                         model="eleven_monolingual_v1")
        print(random_response)
        play(audio)
        subprocess.Popen([app_path[index]])
    except Exception as e:
        error_text = "I'm not really sure what you want me to open here boss?"
        audio = generate(api_key=api_keys[1],
                         text=error_text,
                         voice=voice_id,
                         model="eleven_monolingual_v1")
        print(f'{error_text}: {e}')
        play(audio)


def planned_events():   # She can also tell you that you're late!
    gc.main()
    gc.upcoming_events()

    random_response = random.choice(LC.cal_response)
    response = random_response.format(summary=gc.summary, datetime=gc.formated_datetime)
    audio = generate(api_key=api_keys[1],
                     text=response,
                     voice=voice_id,
                     model="eleven_monolingual_v1"
                     )
    print(response)
    play(audio)


def type_text(text):    # But she can't actually send messages, she just types them out in any text field you have selected... sadge
    import keyboard
    user_input = text
    try:
        response = o_client.chat.completions.create(
            model=LC.gpt_version,
            messages=[
                {
                    "role": "system", "name": "Luna",
                    "content": "Assistant AI"
                },
                {
                    "role": "user",
                    "name": "Boss",
                    "content": user_input
                },
            ],
            temperature=LC.temperature,
            max_tokens=LC.max_tokens,
            top_p=LC.top_p,
            frequency_penalty=LC.freq_pen,
            presence_penalty=LC.pres_pen
        )
        text_to_speak = response.choices[0].message.content
        tts = generate(
            api_key=api_keys[1],
            text=text_to_speak,
            voice=voice_id,
            model='eleven_monolingual_v1'
        )
        play(tts)
        print(f'Luna: {text_to_speak}')
        keyboard.write(f'{text_to_speak} - sent by Luna', delay=0.01)
    except Exception as e:
        print(f"Could not send message: {e}")
