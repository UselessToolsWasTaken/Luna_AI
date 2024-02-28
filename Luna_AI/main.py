import threading    # will be used later
import time         # will be used later
import re
# python module imports

import speech_recognition as sr
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import generate, play, voices
# External library imports

import config   # Runs the config and assigns all the configuration values to their respective variables
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
    # Checks the voice command for what app was mentioned from the function_replies.json
    # and returns the application index, that index is then passed over to the launch_app(index) function
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


def voice_commands():   # the heart and sould of Luna's whole system, without this she's just a chatbot
    with sr.Microphone() as source:
        recognizer.energy_threshold = LC.threshold
        print("Luna is online...")
        while True:
            raudio = recognizer.listen(source)  # initializes the listening for commands as raudio
            try:
                text = recognizer.recognize_google(raudio)  # takes the audio and runs it through googles recognizer and passes it to a text variable
                print(f'Command: {text}')
                if check_trigger(text, LC.luna_talks):      # Here's a bunch of elif's that check the speech to text for any recognizable command using check_trigger()
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
                elif re.search(text, 'quit', re.IGNORECASE):    # Quit option, in case you want Luna to turn off.... Why would you though?
                    break
            except sr.UnknownValueError:    # Some basic error handling
                print('command not recognized')
            except sr.RequestError as e:
                print(f'Could not request result from speech recognition services: {e}')


def talk_with_luna(voice_input):    # GPT part of luna, this is also sprinkled in other functions throughout so i'm not going to explain it every time
    user_input = voice_input
    response = o_client.chat.completions.create(
        model=LC.gpt_version,
        messages=[
            {
                "role": "system", "name": "Luna",
                "content": "Assistant AI"           # Sets Luna to recognize herself as your assistant
            },
            {
                "role": "user",
                "name": "Boss",
                "content": user_input               # Takes user input that's been passed from the speech to text system above
            },
        ],
        temperature=LC.temperature,                 # Some GPT configs, check config.py for more
        max_tokens=LC.max_tokens,
        top_p=LC.top_p,
        frequency_penalty=LC.freq_pen,
        presence_penalty=LC.pres_pen
    )
    text_to_speak = response.choices[0].message.content     # assigns response to a string variable
    tts = generate(
        api_key=api_keys[1],
        text=text_to_speak,
        voice=voice_id,
        model='eleven_monolingual_v1'
    )
    play(tts)
    print(f'Luna: {text_to_speak}')                         # Yare yare bim bam boom, response... Yes, it's that simple


if __name__ == "__main__":
    voice_commands()
# Do I have to explain the above?
