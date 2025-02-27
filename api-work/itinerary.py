import json
import os
from google import genai
from location import get_random_travel_destination_name

import dotenv


l = dotenv.dotenv_values('.env')

# Set your Gemini API key (as before, use environment variables for security)
client = genai.Client(api_key=l['gemini'])

def get_travel_itinerary(destination, days_of_travel, budget=None):
    """Generates a travel itinerary using Gemini with popular excursions."""

    prompt = f"Create a detailed travel itinerary for a trip to {destination} lasting {days_of_travel} days.  Focus on including the most popular and highly-rated excursions and activities in the area."

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
                }
            )

            try:
                itinerary_json = json.loads(str(response.text))
                return itinerary_json
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Raw response: {response.text}")
                continue

        except Exception as e:
            print(f"Error generating itinerary: {e}")
            continue


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