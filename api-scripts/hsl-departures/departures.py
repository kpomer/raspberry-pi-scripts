import sys

# Script will retrieve the next HSL departures for a particular Stop ID

def get_hsl_departures(stop_id):

    return f"Returning departures for STOP_ID: {stop_id}!"


# Check if an argument was provided.
# Call get_hsl_departures() function
if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Get the parameter from the command line
        stop_id = sys.argv[1]
        # Call the function with the provided parameter
        message = get_hsl_departures(stop_id)
        # Print the returned string
        print(message)
    else:
        print("Invalid Input: Must provide 1 parameter for 'STOP_ID'")