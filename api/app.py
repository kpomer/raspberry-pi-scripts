# api/app.py
from flask import Flask, request, jsonify

#Import Blueprints
from hello_world.helloWorld import helloWorld_bp
from current_time.time import currentTime_bp
from hsl_departures.departures import hsl_departures_bp

app = Flask(__name__)

app.register_blueprint(currentTime_bp, url_prefix='/time')
app.register_blueprint(helloWorld_bp, url_prefix='/hello')
app.register_blueprint(hsl_departures_bp, url_prefix='/hsl_departures')

@app.route('/')
def index():
    """Simple root health check to show the service is running."""
    return jsonify({
        "status": "online",
        "server": "pomerpi01",
        "availableServices": ["/time", "/hello", "/hsl_departures"]
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 