from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import json
from completionCall import call_playlist_prompt
import os #provides ways to access the Operating System and allows us to read the environment variables

# load_dotenv()

my_id = os.getenv("ID")
my_secret_key = os.getenv("SECRET_KEY")

app = Flask(__name__)
api = Api(app)
CORS(app)


class status (Resource):
    def get(self):
        try:
            return {'data': 'Api is Running', 'key' : my_secret_key}
        except:
            return {'data': 'An Error Occurred during fetching Api'}


class Sum(Resource):
    def get(self, a, b):
        return jsonify({'data': a+b})
    def post(self):
        data = request.json()
        if 'a' in data and 'b' in data:
            a = data['a']
            b = data['b']
            return jsonify({'data': data})
        else:
            return jsonify({'error': 'Invalid input'}), 400
  
class Moody(Resource):
    def post(self):
        data=request.get_json()
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
        return jsonify(playlist)



class PostExample(Resource):
    def post(self):
        data = request.get_json()  # Get JSON data from the request
        return jsonify(data)  # Echo back the received JSON data



api.add_resource(status, '/')
api.add_resource(Sum, '/add/<int:a>,<int:b>')
api.add_resource(Moody, '/moodymusic')
api.add_resource(PostExample, '/post-example')

if __name__ == '__main__':
    app.run()

