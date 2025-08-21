from flask import Blueprint, jsonify
import datetime

currentTime_bp = Blueprint('time_bp', __name__)

@currentTime_bp.route('/')
def getCurrentTime():
    """
    API endpoint to return the current datetime
    Accessible via /hello/<your_name> (e.g., /hello/Kevin)
    """

    curDateTime = datetime.datetime.now()

    # Return the personalized greeting
    return jsonify({"Time": str(curDateTime)})

