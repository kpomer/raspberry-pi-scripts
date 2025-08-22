# api/hello_world/helloWorld.py
from flask import Blueprint, jsonify, request

helloWorld_bp = Blueprint('hello_world_bp', __name__)

@helloWorld_bp.route('/')
def hello_world():
    # API endpoint to return a personalized 'Hello, {name}!' message.
    # Accesible via /hello/?name={name} using query parameter

    name = request.args.get('name', 'World') #Default value 'World'
    return jsonify({"message": f"Hello, {name} from your Pi API!"})