# transit_api/app.py
from flask import Flask, request, jsonify
from departures2 import get_hsl_departures

app = Flask(__name__)

@app.route('/transit/<stop_id>', methods=['GET'])
def get_transit_info(stop_id):
    """
    API endpoint to get transit departures.
    """
    departures = get_hsl_departures(stop_id)
    return jsonify({"departures": departures})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)