from flask import request
from dotenv import dotenv_values
import openai
import json
import os #provides ways to access the Operating System and allows us to read the environment variables

# load_dotenv()

my_id = os.getenv("ID")
my_secret_key = os.getenv("SECRET_KEY")

 
openai.api_key = my_secret_key
 

def call_playlist_prompt():
    data = request.get_json()  # Parses the JSON data and returns a Python dictionary
    count = data.get('count')
    prompt = data.get('prompt')
    example_json = """
        [
        {"song": "Sexyback", "artist": "Justin Timberlake"},
        {"song": "Pony", "artist": "Ginuwine"},
        {"song": "Talk Dirty", "artist": "Jason Derulo ft. 2 Chainz"},
        {"song": "I'm a Slave 4 U", "artist": "Britney Spears"},
        {"song": "Partition", "artist": "Beyoncé"},
        {"song": "Earned It", "artist": "The Weeknd"},
        {"song": "Buttons", "artist": "The Pussycat Dolls"},
        {"song": "Motivation", "artist": "Kelly Rowland"},
        {"song": "Slow Motion", "artist": "Trey Songz"},
        {"song": "Pillowtalk", "artist": "Zayn"}
        ]
    """

    messages = [
    {"role" : "system", "content" : """You are a helpful playlist generating assistant. You should generate a list of songs and their artists according to a text prompt. You should return a JSON array where each element follows this format: {"song" : <song_title>, "artist" : <artist_name>}"""},
    {"role": "user", "content" : "Generate a list 10 of songs based on this prompt:  love songs"}, 
    {"role" : "assistant", "content" : example_json},
    {"role": "user", "content" : f"Generate a list of {count} songs based on this prompt: {prompt}"}, 
    ]


    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=400,
    )

    playlist = json.loads(completion.choices[0].message.content)
    return playlist