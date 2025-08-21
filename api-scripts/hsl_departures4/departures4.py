import requests
import json
import datetime
import os
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

# Flask Blueprint Setup
hsl_departures_bp = Blueprint('hsl_departures_bp', __name__)

@hsl_departures_bp.route('/')
def get_hsl_departures_api():
    """
    API endpoint to get transit departures.
    Expects 'stop_ids' as a comma-separated string in the query parameters.
    Example: /transit/?stop_ids=HSL:1203402,HSL:1201601
    """
    stop_ids = request.args.get("stop_ids") # Get stop_ids from query parameters

    # Fetch and format the departures data
    # departures_result = fetch_and_format_departures(stop_ids)