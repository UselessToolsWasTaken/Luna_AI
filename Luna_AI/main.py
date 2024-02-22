# import os
# import elevenlabs.core.jsonable_encoder
# import openai as opai
from openai import OpenAI
import re
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
from elevenlabs import generate, play, voices, client, voice
import useful_functions

api_keys = []
voice_id = 'fZBVYnkF2DCL33sbSoHN'
api_path = 'C:\\Users\\evryt\\OneDrive\\Documents\\WorkProjectTXTs\\API Keys\\api_keys.txt'

with open(api_path, "r") as file:
    for line in file:
        api_keys.append(line.strip())  # Reads from a txt file on your system and appends the keys to the list api_keys

o_client = OpenAI(
    api_key=api_keys[0]
)
eleven = ElevenLabs(
    api_key=api_keys[1]
)  # Setting the API keys into the system

application_list = ["island", "chrome", "discord", ]

# Trigger sentences for luna to react on when spoken to.
trigger_sentence = "hey luna"
tell_time = "luna what is the time"
open_application = "luna start"

recognizer = sr.Recognizer()

voices = voices()


def voiceCommands():  # The main loop that runs until the command 'Quit' Has been registered.
    audio = generate(api_key=api_keys[1],
                     text="Hello there! You're now talking to Luna. Say 'quit', to exit the conversation",
                     voice=voice_id,
                     model="eleven_monolingual_v1"
                     )
    play(audio)  # Plays a welcome message
    global text
    global application_value
    with sr.Microphone() as source:
        recognizer.energy_threshold = 2000
        print("You're now talking to Luna, say 'quit' to exit the conversation")  # This initializes the speech
        # recognition
        while True:
            print("New Command input...")
            raudio = recognizer.listen(source, timeout=15)  # Start the listener at the start of the loop and add a
            # 10 second timeout
            try:
                text = recognizer.recognize_google(raudio)  # recognize speech using google speech recognition
                print("You said: " + text)  # printing what was said, mostly for debugging purposes
                if text.lower() == 'quit':  # Quit option, breaks the loop and turns off the app
                    quit_audio = generate(
                        api_key=api_keys[1],
                        text="Goodbye Boss! Have a Pleasant day!",
                        voice=voice_id,
                        model="eleven_monolingual_v1"
                    )
                    play(quit_audio)
                    break
                elif re.search(trigger_sentence, text,
                               re.IGNORECASE):  # If no specific command is called, run the talk function to use GPT 3.5 responses
                    talk_with_luna(text)
                elif re.search(open_application, text, re.IGNORECASE):          # this is the application launch logic
                    if re.search(application_list[0], text, re.IGNORECASE):     # No, I do not intend to use a more efficient way
                        useful_functions.application_value = 0                  # At this point in time i don't even know if it works xD P.S It's working
                        useful_functions.launch_app()
                    elif re.search(application_list[1], text, re.IGNORECASE):
                        useful_functions.application_value = 1
                        useful_functions.launch_app()
                    elif re.search(application_list[2], text, re.IGNORECASE):
                        useful_functions.application_value = 2
                        useful_functions.launch_app()
                elif re.search(tell_time, text, re.IGNORECASE):
                    useful_functions.what_time()
            except sr.UnknownValueError:  # Below is just some error handling
                print("command not recognized")
            except sr.RequestError as e:
                print(f"Could not request results from speech recognition services; {e}")
            except sr.WaitTimeoutError:
                print("I'm waiting...")


def talk_with_luna(voice_input):  # Lunas heart & soul. This is where her magic is done, she responds
    user_input = voice_input  # to you based on her set name and content(Personality)
    response = o_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", "name": "Luna",
                "content": "You're happy to help with anything Boss wants. You're speaking in a happy tone, sometimes "
                           "a bit sarcastic and insert jokes in your sentences"
            },
            {
                "role": "user",
                "name": "Boss",
                "content": user_input
            },
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text_to_speak = response.choices[0].message.content
    tts = generate(
        api_key=api_keys[1],
        text=text_to_speak,
        voice=voice_id,
        model="eleven_monolingual_v1"
    )
    play(tts)
    print("Luna: ", text_to_speak)


if __name__ == "__main__":
    voiceCommands()