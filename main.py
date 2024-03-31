from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv
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
        return call_playlist_prompt()


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

