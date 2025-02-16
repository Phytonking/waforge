import json
import os
from google import genai

import dotenv


l = dotenv.dotenv_values('.env')


# Set your Gemini API key (as before, use environment variables for security)
client = genai.Client(api_key=l['gemini'])

def get_random_travel_destination_name():
    """Asks Gemini for a random travel destination name and returns it as a string."""
    prompt = "Suggest a random travel destination name."  # Very simple prompt
    while True:
        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents="Suggest a random travel destination name that is real. Return in json format with no markdown. Don't use a location you previously used. ",
                config={
                    'response_mime_type': 'application/json',
                }
            )
            print(response.text)

            return json.loads(response.text)["destination"]

        except Exception as e:
            print(f"Error getting destination: {e}")
            continue

"""
# Example usage:
print(get_random_travel_destination_name())
"""