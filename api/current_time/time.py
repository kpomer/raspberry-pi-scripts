# api/current_time/time.py
from flask import Blueprint, jsonify
import datetime

currentTime_bp = Blueprint('time_bp', __name__)

@currentTime_bp.route('/')
def getCurrentTime():
    # API endpoint to return the current datetime

    curDateTime = datetime.datetime.now()

    return jsonify({"Time": str(curDateTime)})

