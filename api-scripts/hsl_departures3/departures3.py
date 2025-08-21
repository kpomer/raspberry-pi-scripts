import sys
import requests
import json
import datetime
import os
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

hsl_departures_bp = Blueprint('hsl_departures_bp', __name__)

# Gather values from .env file stored in root folder
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_ENDPOINT = os.getenv("API_ENDPOINT")

headers = {
    'Content-Type': 'application/graphql'
}
parameters = {
    'digitransit-subscription-key': API_KEY
}

@hsl_departures_bp.route('/')
def get_hsl_departures():
    responseData = ""
    stop_ids = request.args.get("stop_ids")

        # Check if the required environment variables are set.
    if not API_KEY or not API_ENDPOINT:
        responseData = FormatResponse(responseData, "Error: Required environment variables are missing.")
        responseData = FormatResponse(responseData, "Please ensure API_KEY and API_ENDPOINT are set in your .env file")
        return jsonify({"Departures": responseData})

    try:
        # Make the POST request to the API with the GraphQL query.
        response = requests.post(API_ENDPOINT, params=parameters, headers=headers, data=getGraphQL_query(stop_ids))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        # Check if the data contains the expected structure.
        if "data" not in data or data["data"]["stops"] is None:
            responseData = FormatResponse(responseData, "Error: Could not retrieve stop data. Please check the stop ID or API key.")
            return jsonify({"Departures": responseData})

        stop_data = data["data"]["stops"]
        for s in stop_data:
                
            stop_name = s["name"]
            vehicle_mode = s["vehicleMode"]
            departures = s["stoptimesWithoutPatterns"]

            # print(f"\nNext departures for {vehicle_mode} stop: {stop_name}:") # Extended text length
            responseData = FormatResponse(responseData, f"\n{vehicle_mode} {stop_name}:") # Shortened text length

            if not departures:
                responseData = FormatResponse(responseData, "No upcoming departures found.")
                return jsonify({"Departures": responseData})

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
                destination = departure["headsign"]

                # print(f"  {i+1}. Line {transit_number} to {destination} at {departure_time} - ({time_to_departure})") # Extended text length
                # print(f"{transit_number} to {destination} at {departure_time} - ({time_to_departure})") # Shortened text length
                responseData = FormatResponse(responseData, f"{transit_number} at {departure_time} - ({time_to_departure})") # Super-short text length

    except requests.exceptions.RequestException as e:
        # Check for specific 401 error and provide a more helpful message.
        if e.response and e.response.status_code == 401:
            responseData = FormatResponse(responseData, "Error: 401 Unauthorized. The API key is likely missing, incorrect, or expired.")
        elif e.response and e.response.status_code == 404:
            responseData = FormatResponse(responseData, "Error: 404 Not Found. The API endpoint may be incorrect or deprecated.")
            responseData = FormatResponse(responseData, "The code has been updated to use the correct endpoint. Please try again.")
        else:
            responseData = FormatResponse(responseData, f"An error occurred while connecting to the API: {e}")
    except json.JSONDecodeError:
        responseData = FormatResponse(responseData, "Error: The API response was not valid JSON.")
    except KeyError as e:
        responseData = FormatResponse(responseData, f"Error: Missing key in API response data: {e}")

    return jsonify({"Departures": responseData})

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


def FormatResponse(responseData, newData):
    if(responseData != ""):
        responseData += "\n"
    responseData += newData
    return responseData