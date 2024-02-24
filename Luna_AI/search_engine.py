import webbrowser
import json
import random

input_text = None

def load_file(filename=r"C:\Users\evryt\PycharmProjects\Luna_AI\memory\function_replies.json"):
    global input_text
    with open(filename, 'r') as file:
        data = json.load(file)
        input_text = data['Google Search']['responses']

def search_the_web(query):
    from elevenlabs.client import ElevenLabs
    from elevenlabs import generate, play, voices, client
    import main as mn
    api_keys = mn.api_keys
    eleven = ElevenLabs(
    api_key=api_keys[1]  # Defaults to ELEVEN_API_KEY
    )
    try:
        query_encoded = query.replace(' ', '+') # Encoding the query for a URL
        search_voice = random.choice(input_text)
        joke_audio = generate(api_key=api_keys[1],
                            text=search_voice,
                            voice=mn.voice_id,
                            model="eleven_monolingual_v1"
                            )
        play(joke_audio)
        url = f"https://www.google.com/search?q={query_encoded}"
        webbrowser.open(url)
    except Exception as e:
        print(f'Error when googling, {e}')
