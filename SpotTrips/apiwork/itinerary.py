import json
import os
from google import genai
from apiwork.location import get_random_travel_destination_name
from datetime import datetime
import dotenv


l = dotenv.dotenv_values('.env')

# Set your Gemini API key (as before, use environment variables for security)
client = genai.Client(api_key=l['gemini'])

def get_travel_itinerary(destination, days_of_travel, budget=None, depart_from=None):
    """Generates a travel itinerary using Gemini with popular excursions."""

    prompt = f"Create a detailed travel itinerary for a trip to {destination} from {depart_from} lasting {days_of_travel} days.  Focus on including the most popular and highly-rated excursions and activities in the area. This plan must only include flights and hotels from the origin to the destination. "

    if budget:
        prompt += f" The budget for the trip is {budget}."  # Keep budget option if desired

    prompt += " Please provide the itinerary in JSON text with the following structure. Return in json format with no markdown.:\n"
    prompt += """
    {
      "destination": "string",
      "days_of_travel": integer,
      "itinerary": [
        {
          "day": integer,
          "travel_day": boolean,
          "excursions": [
            "string",  // Name of excursion/activity
            "string",
            ...
          ],
          "restaurants": {  // Could make this optional in prompt if needed
            "breakfast": "string",
            "lunch": "string",
            "dinner": "string"
          }
        },
        {
          "day": integer,
          "travel_day": boolean,
          "excursions": [],
          "restaurants": {}
        },
        ...
      ]
    }
    """
    while True:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'temperature': 0.8
                }
            )
            
            itinerary_json = json.loads(str(response.text))
            return json.dumps(itinerary_json)
        except Exception as e:
            print(f"Error generating itinerary: {e}")
            import time
            time.sleep(0.5)
            continue


def days_of_travel_calc(from_date, to_date):
    date_format = "%Y-%m-%d"
    
        # Convert the string dates to datetime objects
    date1 = datetime.strptime(from_date, date_format)
    date2 = datetime.strptime(to_date, date_format)
        
        # Calculate the difference in days
    delta = date2 - date1
        
    return delta.days

"""
# Example usage:
destination = get_random_travel_destination_name() # Example
days_of_travel = 4
budget = "$800-$1200" # Example

itinerary_json = get_travel_itinerary(destination, days_of_travel)

if itinerary_json:
    print(itinerary_json)
    # Process the JSON data:
    # itinerary_data = json.loads(itinerary_json)
    # ...
else:
    print("Failed to generate itinerary.")
"""