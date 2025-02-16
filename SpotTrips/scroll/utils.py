import json
import os
from google import genai
from apiwork.location import get_random_travel_destination_name
from datetime import datetime
import dotenv
from web.models import *
from apiwork.location import get_random_travel_destination_name
import time
from apiwork.api import *


l = dotenv.dotenv_values('.env')

# Set your Gemini API key (as before, use environment variables for security)
client = genai.Client(api_key=l['gemini'])

def make_new_post():
    location = get_random_travel_destination_name()
    prompt = f"Find 3 keywords for images of wellknown places in {location} and make a description of {location}."
    prompt += f" Please provide the itinerary in JSON text with the following structure, DO NOT PUT THE JSON IN A LIST. Return in json format with no markdown. THERE SHOULD ONLY BE ONE LOCATION which is the {location}:\n"
    prompt += """
    {
        "location": "",
        "description": "",
        "images": [
            "tower of piza",
            "coloseeum"
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
                    'temperature': 0.2
                }
            )
            print(str(response.text))
            itinerary_json = json.loads(str(response.text))
            itinerary_json["images"] = get_first_images(itinerary_json["images"])
            print(itinerary_json)
            return json.dumps(itinerary_json)
        except Exception as e:
            print(f"Error generating itinerary: {e}")
            time.sleep(1)
            continue
            