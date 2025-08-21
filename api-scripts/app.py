# transit_api/app.py
from flask import Flask, request, jsonify

#Import Blueprints
from hello_world.helloWorld import helloWorld_bp
from current_time.time import currentTime_bp
from hsl_departures3.departures3 import hsl_departures_bp

app = Flask(__name__)

app.register_blueprint(currentTime_bp, url_prefix='/time')
app.register_blueprint(helloWorld_bp, url_prefix='/hello')
app.register_blueprint(hsl_departures_bp, url_prefix='/hsl_departures')

@app.route('/')
def index():
    """Simple root route to show the API is running."""
    return jsonify({"message": "Welcome to your Raspberry Pi API!"})

# @app.route('/transit/<stop_id>', methods=['GET'])
# def get_transit_info(stop_id):
#     """
#     API endpoint to get transit departures.
#     """
#     departures = get_hsl_departures(stop_id)
#     return jsonify({"departures": departures})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)