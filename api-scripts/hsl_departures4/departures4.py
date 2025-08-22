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
    Example: /transit/?stop_ids=HSL:1111111,HSL:2222222
    """
    stop_ids = request.args.get("stop_ids") # Get stop_ids from query parameters

    # Gather formatted departures data
    departures_result = retrieveFormattedDepartures(stop_ids)

    # Check if the result string indicates an error
    if departures_result.startswith("Error:"):
        # Extract potential status code from error message for better handling
        if "400" in departures_result:
            return jsonify({"responseData": departures_result}), 400
        elif "401" in departures_result:
            return jsonify({"responseData": departures_result}), 401
        elif "404" in departures_result:
            return jsonify({"responseData": departures_result}), 404
        else:
            # Generic server error for other unexpected issues
            return jsonify({"responseData": departures_result}), 500
    
    # If no "Error:" prefix, assume success and return 200 OK
    return jsonify({"responseData": departures_result}), 200


# Gather values from .env file stored in same directory

# Construct the path to the .env file relative to the current script's location.
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
API_KEY = os.getenv("API_KEY")
API_ENDPOINT = os.getenv("API_ENDPOINT")

headers = {
    'Content-Type': 'application/graphql'
}
parameters = {
    'digitransit-subscription-key': API_KEY
}

def retrieveFormattedDepartures(stop_ids):

    output_lines = [] # Local list to accumulate response parts

    # Validate required variables and parameters
    if not API_KEY or not API_ENDPOINT:
        return "Error: Required environment variables (API_KEY, API_ENDPOINT) are missing. Please check your .env file."
    elif not stop_ids or not isinstance(stop_ids, str) or not stop_ids.strip():
        return "Error: Invalid input. 'stop_ids' query parameter must be a non-empty, comma-separated string (e.g., 'HSL:1111111,HSL:2222222')."

    try:
        query = getGraphQL_query(stop_ids)
        if query is None:
            return f"Error: Failed to generate GraphQL query due to invalid stop_ids format: {stop_ids}"

        # Make the POST request to the API with the GraphQL query.
        response = requests.post(API_ENDPOINT, params=parameters, headers=headers, data=query)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        # Check if the data contains the expected structure.
        if "data" not in data or data["data"]["stops"] is None:
            return "Error: Could not retrieve stop data. Please check the stop ID or API key."

        stop_data = data["data"]["stops"]
        if not stop_data or stop_data == [None]:
            return "No stop data found for the provided stop_ids"
        
        for s in stop_data:
                
            stop_name = s["name"]
            vehicle_mode = s["vehicleMode"]
            departures = s["stoptimesWithoutPatterns"]

            output_lines.append(f"\n{vehicle_mode} {stop_name}:")

            if not departures:
                output_lines.append("No upcoming departures found.")
                continue

            for i, departure in enumerate(departures):
                # The API returns departure time as a number of seconds from the beginning of the current day.
                departure_timestamp_seconds = departure["realtimeDeparture"]
                start_of_day = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                departure_datetime = start_of_day + datetime.timedelta(seconds=departure_timestamp_seconds)
                current_datetime = datetime.datetime.now()

                # Calculate time until departure in minutes
                seconds_to_departure = (departure_datetime - current_datetime).seconds
                time_to_departure = ""
                if(seconds_to_departure > 0):
                    time_to_departure = f"{seconds_to_departure // 60} min"
                else:
                    time_to_departure = "DEPARTED"

                # Format the correctly calculated datetime object into a readable time string.
                # departure_time = departure_datetime.strftime('%H:%M:%S') # Full timestamp H:M:S
                departure_time = departure_datetime.strftime('%H:%M') # Shortened timestamp H:M
                # Extract the transit line number and destination.
                transit_number = departure["trip"]["route"]["shortName"]
                # destination = departure["headsign"]

                # print(f"  {i+1}. Line {transit_number} to {destination} at {departure_time} - ({time_to_departure})") # Extended text length
                # print(f"{transit_number} to {destination} at {departure_time} - ({time_to_departure})") # Shortened text length
                output_lines.append(f"{transit_number} at {departure_time} - ({time_to_departure})") # Super-short text length

    except requests.exceptions.RequestException as e:
        # Check for specific 401 error and provide a more helpful message.
        if e.response and e.response.status_code == 401:
            return "Error: 401 Unauthorized. The API key is likely missing, incorrect, or expired."
        elif e.response and e.response.status_code == 404:
            return "Error: 404 Not Found. The API endpoint may be incorrect or deprecated."
        else:
            return f"An error occurred while connecting to the API: {e}"
    except json.JSONDecodeError:
        return "Error: The API response was not valid JSON."
    except KeyError as e:
        return f"Error: Missing key in API response data: {e}"
    except Exception as e: # <-- Catchall for any other unexpected exceptions
        return f"Error: An unexpected internal error occurred: {e}"
    
    return "\n".join(output_lines)

def getGraphQL_query(stop_ids):
        
    # stop_ids variable supports a single stop (ex. "HSL:11235") or multiple stops in csv format (ex. "HSL:11235,HSL:81321")
    query = """
        {
        stops(ids: ["%s"]) {
            name
            vehicleMode
            stoptimesWithoutPatterns(numberOfDepartures: 5, omitNonPickups: true) {
            realtimeDeparture
            headsign
            trip {
                route {
                shortName
                }
            }
            }
        }
        }
        """ % "\", \"".join(stop_ids.split(",")) #Format stop_ids for GraphQL query
    
    return query