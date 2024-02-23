import random

from elevenlabs.client import ElevenLabs
from elevenlabs import generate, play, voices, client
import json
import subprocess
import main
import random as r
import google_callendar as gc
from openai import OpenAI

api_keys = main.api_keys
text = None

eleven = ElevenLabs(
    api_key=api_keys[1]  # Defaults to ELEVEN_API_KEY
)
o_client = OpenAI(
    api_key=api_keys[0]
)
launched_app = [r'C:\Program Files\Island\Island\Application\Island.exe',
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Users\evryt\AppData\Local\Discord\app-1.0.9033\Discord.exe']

interactions = []

application_value = 0

cal_res, time_res = None, None


def load_triggers(filename=r"C:\Users\evryt\PycharmProjects\Luna_AI\memory\function_replies.json"):
    global time_res, cal_res
    with open(filename, 'r') as file:
        data = json.load(file)
        time_res = data['Time Request']['response']
        cal_res = data['Calendar Request']['response']


# Telling the Time
def what_time():
    from datetime import datetime
    random_time_response = random.choice(time_res)
    current_time = datetime.now()
    ai_time = current_time.strftime("%I:%M %p")
    time_sentence = random_time_response.format(time=ai_time)
    time_audio = generate(api_key=api_keys[1],
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
        island_audio = generate(api_key=api_keys[1],
                                text=launch_sentence,
                                voice=main.voice_id,
                                model="eleven_monolingual_v1"
                                )
        print(launch_sentence)
        play(island_audio)
    except Exception as e:
        island_error = "I'm not really sure what you want me to open here boss?"
        error_audio = generate(api_key=api_keys[1],
                               text=island_error,
                               voice=main.voice_id,
                               model="eleven_monolingual_v1"
                               )
        print(island_error, e)
        play(error_audio)


def unprompted_interaction_joke():
    global interactions
    interaction_path = r'C:\Users\evryt\PycharmProjects\Luna_AI\interactions_doc.txt'
    try:
        with open(interaction_path, "r") as file:
            for line in file:
                interactions.append(line.strip())
        random_interaction = r.randint(0, 4)
        joke_audio = generate(api_key=api_keys[1],
                              text=interactions[random_interaction],
                              voice=main.voice_id,
                              model="eleven_monolingual_v1"
                              )
        print(interactions[random_interaction])
        play(joke_audio)
    except Exception as e:
        print(f"Could not run command {e}")


def planned_events():
    gc.main()
    gc.upcoming_events()
    rand_cal_res = random.choice(cal_res)
    cal_sentence = rand_cal_res.format(summary=gc.summary, datetime=gc.formated_datetime)
    # Finish implementing the calendar functionality
    event_audio = generate(api_key=api_keys[1],
                           text=cal_sentence,
                           voice=main.voice_id,
                           model="eleven_monolingual_v1"
                           )
    event_text = cal_sentence
    play(event_audio)
    print(event_text)


def type_for_me():
    import keyboard
    user_input = text  # to you based on her set name and content(Personality)
    try:
        response = o_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", "name": "Luna",
                    "content": "You're happy to help with anything Boss wants. You're speaking in a happy tone, "
                               "sometimes"
                               "a bit sarcastic and insert jokes in your sentences"
                },
                {
                    "role": "user",
                    "name": "Boss",
                    "content": user_input
                },
            ],
            temperature=0.6,
            max_tokens=256,
            top_p=0.7,
            frequency_penalty=0.2,
            presence_penalty=0.2
        )
        text_to_speak = response.choices[0].message.content
        tts = generate(
            api_key=api_keys[1],
            text=text_to_speak,
            voice=main.voice_id,
            model="eleven_monolingual_v1"
        )
        play(tts)
        print("Luna: ", text_to_speak)
        keyboard.write(f'{text_to_speak} - Sent by Luna', delay=0.01)
    except Exception as e:
        print(f"Could not send message: {e}")
