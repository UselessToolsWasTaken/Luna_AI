import json
import main as mn

def load_memory_triggers(filename=r"C:\Users\evryt\PycharmProjects\Luna_AI\memory\function_replies.json"):
    with open(filename, 'r') as file:
        data = json.load(file)
        mem_triggers = data['memory triggers']['memorize']
        like_triggers = data['memory triggers']['mem']['likes']

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