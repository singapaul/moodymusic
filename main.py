from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables

load_dotenv()

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


api.add_resource(status, '/')
api.add_resource(Sum, '/add/<int:a>,<int:b>')

if __name__ == '__main__':
    app.run()