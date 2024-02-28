import threading
import time
import re
# python module imports

import speech_recognition as sr
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import generate, play, voices
# External library imports

import config
from config import LoadConfig as LC
import useful_functions as UF
import search_engine as SE
# internal code imports

api_keys = LC.api_keys
voice_id = LC.voice_ID


def check_trigger(text, triggers):  # Checks for triggers when ran through speech to text
    for trigger in triggers:
        if re.search(trigger, text, re.IGNORECASE):
            return True
    return False


def get_application_index(text):
    applications = LC.app_name
    for index, application in enumerate(applications):
        if application.lower() in text.lower():
            return index
    return None


o_client = OpenAI(
    api_key=api_keys[0]
)
eleven = ElevenLabs(
    api_key=api_keys[1]
)
# Setting the proper API keys from the configuration filee

recognizer = sr.Recognizer()  # initialize recognizer
voices = voices()

audio = generate(api_key=api_keys[1],
                 text='Welcome boss, what can I do for you today?',
                 voice=voice_id,
                 model='eleven_monolingual_v1')
play(audio)  # Play introduction message for the user


def voice_commands():
    with sr.Microphone() as source:
        recognizer.energy_threshold = LC.threshold
        print("Luna is online...")
        while True:
            raudio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(raudio)
                print(f'Command: {text}')
                if check_trigger(text, LC.luna_talks):
                    print('Luna will respond')
                    talk_with_luna(text)
                elif check_trigger(text, LC.tell_time):
                    print('Luna will tell the time')
                    UF.tell_time()
                elif check_trigger(text, LC.open_app):
                    print("Luna will open an app")
                    index = get_application_index(text)
                    if index is not None:
                        print(f'Application ran: {index}')
                        UF.launch_app(index)
                    else:
                        print("Could not run specified app")
                elif check_trigger(text, LC.check_cal):
                    print("Luna will check the calendar")
                    UF.planned_events()
                elif check_trigger(text, LC.send_message):
                    print("Luna will send a message")
                    UF.type_text(text)
                elif check_trigger(text, LC.google_search):
                    print("Luna will search the web")
                    text = text.replace("please google", " ")
                    SE.search_the_web(text)
                elif re.search(text, 'quit', re.IGNORECASE):
                    break
            except sr.UnknownValueError:
                print('command not recognized')
            except sr.RequestError as e:
                print(f'Could not request result from speech recognition services: {e}')


def talk_with_luna(voice_input):
    user_input = voice_input
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


if __name__ == "__main__":
    voice_commands()
