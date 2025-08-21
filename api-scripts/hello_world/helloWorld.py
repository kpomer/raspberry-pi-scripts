# api-scripts/hello_world/helloWorld.py
from flask import Blueprint, jsonify, request

# Create a Blueprint instance
# The first argument is the blueprint's name, the second is its import_name.
# This 'getResponse_bp' is the object you import and register in app.py.
helloWorld_bp = Blueprint('hello_world_bp', __name__)

# Updated route to accept a 'name' parameter
# @helloWorld_bp.route('/<string:name>')
# def hello_world(name):
#     """
#     API endpoint to return a personalized 'Hello, {name}!' message.
#     Accessible via /hello/<your_name> (e.g., /hello/Kevin)
#     """
#     # Return the personalized greeting
#     return jsonify({"message": f"Hello, {name} from your Pi API!"})

@helloWorld_bp.route('/')
def hello_world():
    """
    API endpoint to return a personalized 'Hello, {name}!' message.
    Accessible via /hello/<your_name> (e.g., /hello/Kevin)
    """

    name = request.args.get('name', 'default')
    # Return the personalized greeting
    return jsonify({"message": f"Hello, {name} from your Pi API!"})