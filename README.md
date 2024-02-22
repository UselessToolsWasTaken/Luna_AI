# Welcome to Luna AI

My first long term project that I intend to iterate on over the years, adding more and more functionality.

## What is Luna AI's purpose?

For simplicity's sake I'll refer to Luna as a She, the Ai has a female voice and It's just easier to type this readme this way.

Luna has a few purposes that I planned out ahead of time but no specific direction just yet. The general idea is to have her be as close to a human assistant as possible, either by artificially
making her prompt certain interactions or by as human speech as possible with the current technology. Think of her as a JARVIS, just not AI and less sophisticated.

The long term would be to use her in a smart home, she'd be able to control the houses power grid, sprinkler system, monitor and control power outputs throughout the house as well as control utensils, screens, doors, locks, etc.
I even thought it'd be a good and funny Idea to have her be used in the doorbell camera.

## Explaining Luna's current functionality

Currently, Luna's got 3 main Python scripts running when you turn her on. One is the main.py which is the logic controler, it does everything from recognizing specific commands to just allowing you to prompt Luna to talk with you about anything you want

### Current imports used
os, elevenlabs.core and openai are on standby for the future.
```Python

# import os
# import elevenlabs.core.jsonable_encoder
# import openai as opai
from openai import OpenAI
import re
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
from elevenlabs import generate, play, voices, client, voice
import useful_functions

```

---

### API access key alocation
This is the start of the script. It basically grabs a TXT of the local PC that I placed in a specific folder and reads the lines off from it and appends it to a list. I can then just use the index values of the relevant API keys where needed without putting in the actual KEY into the code.
```Python
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
```

---

### Initializing the commands and voice recognition
In this section we define some commands. In the future I intend to move them into a txt file and append them to a list, this way I wont need to modify the script every time I want to change or add commands

Along with that here we initialize the Voice Recognition from the speech_recognition library and Voices() from the ElevenLabs API
```Python
# Trigger sentences for luna to react on when spoken to.
trigger_sentence = "hey luna"
tell_time = "luna what is the time"
open_application = "luna start"

recognizer = sr.Recognizer()

voices = voices()
```

---

### Where the magic happens...
We're going to break this into parts. This is where the whole voice recognition and commands are processed along with some basic error handling

Below we create a function called voiceCommands(). The function runs on startup, this line is at the end of the main.py script ```Python if __name__ == "__main__": voiceCommands()``` Simple solution. Works well, without any bullshit.

The function starts off by introducing Luna and how to Quit the program entirely. ```global application_value``` is a remnant from a bad solution to running voice commands so you can ignore that. Next we basically "plug in" the microphone for luna
to hear us and we do it as a source. We then add a audio threshold, basically you only want the audio to be recognized when you're loud enough this way Luna doesn't hear you mumbling to yourself.
```Python
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
```

After that we enter the main logic loop of the assistant. This loop listens in, to your microphone with a 15 second timeout. Once the timeout is done it throws an exception WaitTimeoutError. 
The below looks like a lot but it's just a shit ton of if statements and error handling to make sure it's all working well. Python doesn't support switch cases to my knowledge so I had to use elif's here and there... everywhere.

Lets go through this. raudio is the recognizer that listens to your voice input. if you remember we assigned recognizer right at the start of the script. It then uses the google voice recognition (not the cloud one... the bad one that's freed)
and turns it into plain text. That text is then interpreted by the if statements which work sort of like a filter system for keywords.

They check for the presence of any specific string of letters present in ```trigger_sentence```, ```tell_time```,```open_application```. PS. If open application is recognized it then looks for any words present in the ```application_list``` to run the proper functions
If any of those is recognized (other than ```trigger_sentence```) it runs the appropriate function in useful_functions.py.
```Python
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
```

### Chat GPT
This is kinda self explanatory, this is just an implementation of Chat GPT

```Python
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
```