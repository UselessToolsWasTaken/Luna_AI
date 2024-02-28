import webbrowser
import random
from elevenlabs.client import ElevenLabs
from elevenlabs import generate, play, voices, client

from config import LoadConfig as LC

api_keys = LC.api_keys
voice_id = LC.voice_ID

eleven = ElevenLabs(
    api_key=api_keys[1]
)
voices = voices()


def search_the_web(query):
    try:
        query_encoded = query.replace(' ', '+')  # Encoding the query for a URL
        random_response = random.choice(LC.search_responses)
        joke_audio = generate(api_key=api_keys[1],
                              text=random_response,
                              voice=voice_id,
                              model="eleven_monolingual_v1"
                              )
        play(joke_audio)
        print(random_response)
        url = f"https://www.google.com/search?q={query_encoded}"
        webbrowser.open(url)
    except Exception as e:
        print(f'Error when googling, {e}')
