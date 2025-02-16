import json
import os
from google import genai

import dotenv
import time


l = dotenv.dotenv_values('.env')


# Set your Gemini API key (as before, use environment variables for security)
client = genai.Client(api_key=l['gemini'])

def get_random_travel_destination_name():
    """Asks Gemini for a random travel destination name and returns it as a string."""
    prompt = "Imagine you have a world map in front of you. Suggest a random travel destination name that is real. DO NOT PUT THE JSON IN A LIST. Don't use a location you previously used or is too common."
    prompt = """ 
        Use this as an example for the data you should return:
        {
            "destination": ""
        }
    """  # Very simple prompt
    while True:
        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'temperature': 1.5
                }
            )
            print(response.text)

            return json.loads(response.text)["destination"]

        except Exception as e:
            print(f"Error getting destination: {e}")
            time.sleep(0.5)
            continue

"""
# Example usage:
print(get_random_travel_destination_name())
"""