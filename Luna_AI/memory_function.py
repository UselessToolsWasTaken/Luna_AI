import json
import re
from openai import OpenAI
import speech_recognition as sr
import main as mn

'''
You can literally ignore this whole piece of code as it's not implemented yet. It's a major work in progress and I'm expecting
at least 2 to 3 months of constant work to get this running as intended with all the possible things i want Luna to 
remember and recall. It's going to be a chore to deal with, but hey... Cool does not mean easy!
'''


recognizer = sr.Recognizer()

mem_triggers, like_triggers, dislike_triggers, pers_triggers, event_triggers, name_trigger = None, None, None, None, None, None

api_keys = mn.api_keys

o_client = OpenAI(
    api_key=api_keys[0]
)


def load_memory_triggers(filename=r"Path here"):
    global mem_triggers, like_triggers, dislike_triggers, pers_triggers, event_triggers, name_trigger
    with open(filename, 'r') as file:
        data = json.load(file)
        mem_triggers = data['memory triggers']['memorize']
        name_trigger = data['memory triggers']['mem']['name']
        like_triggers = data['memory triggers']['mem']['likes']
        dislike_triggers = data['memory triggers']['mem']['dislikes']
        pers_triggers = data['memory triggers']['mem']['personality']
        event_triggers = data['memory_triggers']['mem']['events']


def check_memory_triggers(text, triggers):
    for trigger in triggers:
        if re.search(trigger, text, re.IGNORECASE):
            return True
    return False


def memory_retention():
    load_memory_triggers()
    with sr.Microphone() as source:
        recognizer.energy_threshold = 4000
        print("What information are we retaining today?")
        while True:
            raudio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(raudio)
                print(f'You said {text}')
            except Exception as e:
                print(f'An error occured: {e}')


'''
This whole area is going to be memory retention and recall. I don't know yet how I'll implement it, but once I do, this comment
will explain it in as much detail as possible.

The general idea is to run Luna's memory like a pipeline, real memory does not work like that and is more like a bookshelf or cupboard with a bunchh of cupboards, or one of those Library cupboards
with the tiny alphabet cards that tell the librarian where to find the book.... Which literally just gave me an idea for that. Lets try it this way.

I will create a JSON file where each section is it's own alphabet card like in a Library. But instead of alphabet letters we're going to use different things that Luna can remember. like
Likes, Dislikes, Names, Places, Situations, Events and whatever else we can think of. I will also add a logic to dynamically add more of those sections through voice commands but that'll come at the end.

{
    "name":{
        "trigger":[],
        "like":{
            "trigger":[],
            "content":[]
        },
        "dislike":{
            "trigger":[],
            "content":[]            
        },
        "personality":{
            "trigger":[],
            "content":[]
        },
        "etc":{
            "etc":[]
        }
    }
}

This is what I came up with. This should work as intended, now lets find a way to make it so that I can save specific pieces of data by saying it in one line and not need one command per object and key
'''
