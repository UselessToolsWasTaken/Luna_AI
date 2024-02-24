from openai import OpenAI
import json
import threading
import time
import re
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
from elevenlabs import generate, play, voices, client, voice
import useful_functions
import google_callendar as gc


# Below are all the Variables currently used by the system.
conv_start, time_request, open_request, calendar_request, send_message, app_names = None, None, None, None, None, None
quit_condition = False
text = None
text_to_speak = None
api_keys = []
voice_id = 'fZBVYnkF2DCL33sbSoHN'
api_path = 'C:\\Users\\evryt\\OneDrive\\Documents\\WorkProjectTXTs\\API Keys\\api_keys.txt'
# ------------------------------------------------------------------------------------------------------------
with open(api_path, "r") as file: # Appending API key from file to api_keys variable
    for line in file:
        api_keys.append(line.strip())  

o_client = OpenAI(
    api_key=api_keys[0]
)   # I don't really need to explain these do I?
eleven = ElevenLabs(
    api_key=api_keys[1]
)   # I don't really need to explain these do I?

recognizer = sr.Recognizer()

voices = voices()

def load_triggers(filename=r"C:\Users\evryt\PycharmProjects\Luna_AI\memory\function_replies.json"): # Reads a JSON file with a set of prompts and stuff, check function_replies.json for more
    global conv_start, time_request, open_request, calendar_request, send_message, app_names
    with open(filename, 'r') as file:
        data = json.load(file)
        conv_start = data['Conversation']['triggers']
        time_request = data['Time Request']['triggers']
        open_request = data['Open Request']['triggers']
        calendar_request = data['Calendar Request']['triggers']
        send_message = data['Send Message']['triggers']
        app_names = data["Open Request"]["applications"]


def check_triggers(text, triggers): # This function runs right after the user speaks and checks the received text from speech for any trigger sentences/words
    for trigger in triggers:
        if re.search(trigger, text, re.IGNORECASE):
            return True
    return False

def check_app(text, application):   # This script reads through the applications in the json and returns the index of a match found by re.search()
    for index, app in enumerate(application):
        if re.search(app, text, re.IGNORECASE):
            return index
    return None

# This is the main meat and potatoes of this system. Luna basically runs in here. 
def voiceCommands(): 
    global quit_condition
    global text
    audio = generate(api_key=api_keys[1],
                     text="Hello there! You're now talking to Luna. Say 'quit', to exit the conversation",
                     voice=voice_id,
                     model="eleven_monolingual_v1"
                     )
    play(audio) # Short welcome message
    global text
    global application_value
    load_triggers()                     # See load_triggers function
    useful_functions.load_triggers()    # See load_triggers in useful_functions.py
    with sr.Microphone() as source:
        recognizer.energy_threshold = 4000  # Microphone sensitivity, the number has no unit and I've chosen this one as it works best for my microphone
        print("You're now talking to Luna, say 'quit' to exit the conversation")  
        # recognition
        while True: # The loop begins, First we initiate the listening part of speech_recognition, then we run it through googles speech recognition service
            print("New Command input...")
            raudio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(raudio)  # Parses the voice input into a string
                print("You said: " + text)  
                if text.lower() == 'quit':  # Simple quit function, currently not working as there's other loops independent of it.
                    quit_audio = generate(
                        api_key=api_keys[1],
                        text="Goodbye Boss! Have a Pleasant day!",
                        voice=voice_id,
                        model="eleven_monolingual_v1"
                    )
                    play(quit_audio)
                    quit_condition = True
                    break
                elif check_triggers(text, conv_start):          # Not gonna run each one solo, this is basically
                    talk_with_luna(text)                        # Where Luna decides what she will do based on your input
                elif check_triggers(text, time_request):        # Luna will understand multiple pre-defined 'trigger sentences'
                    useful_functions.what_time()                # and act based on how she was programmed. All of those can be found in function_replies.json
                elif check_triggers(text, calendar_request):
                    useful_functions.planned_events()
                elif check_triggers(text, send_message):
                    useful_functions.text = text
                    useful_functions.type_for_me()
                elif check_triggers(text, open_request):
                    useful_functions.application_value = check_app(text, app_names) # Assigns the index of the application mentioned to the application_value in useful_functions.py
                    useful_functions.launch_app()
            except sr.UnknownValueError:
                print("command not recognized")
            except sr.RequestError as e:
                print(f"Could not request results from speech recognition services; {e}")

# This is the GPT system in the background. If no specific command is used, Luna will respond using this (Exception is the type_out_message function in useful_functions)
def talk_with_luna(voice_input):  
    global text_to_speak
    user_input = voice_input 
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
        voice=voice_id,
        model="eleven_monolingual_v1"
    )
    play(tts)
    print("Luna: ", text_to_speak)


def countdown_for_interaction():
    global quit_condition
    while True:
        if quit_condition is False:
            time.sleep(5 * 60)
            try:
                useful_functions.unprompted_interaction_joke()
            except Exception as e:
                print(f'could not run function {e}')
        else:
            break


luna_main_thread = threading.Thread(target=voiceCommands)
rand_interaction_thread = threading.Thread(target=countdown_for_interaction)

if __name__ == "__main__":
    luna_main_thread.start()
    rand_interaction_thread.start()
