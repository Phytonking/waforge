import json
import os
from google import genai
from apiwork.location import get_random_travel_destination_name
from datetime import datetime
import requests
import dotenv


l = dotenv.dotenv_values('.env')


def find_flights(departure, destination, departure_date, arrival_date):
    k = requests.get(f"https://serpapi.com/search.json?engine=google_flights&departure_id={departure}&arrival_id={destination}&gl=us&hl=en&currency=USD&outbound_date={departure_date}&return_date={arrival_date}&api_key={l['api']}")
    return k.json()['best_flights'][0]

def find_hotels(location, from_date, to_date, max_price):
    k = requests.get(f"https://serpapi.com/search.json?engine=google_hotels&q={location} hotels&gl=us&hl=en&currency=USD&check_in_date={from_date}&check_out_date={to_date}&sort_by=8&min_price=50&max_price={max_price}&rating=8&api_key={l['api']}")
    return k.json()['properties'][0]

def find_local_spots(location, excusion_type):
    k = requests.get(f"https://serpapi.com/search.json?engine=google_local&q={excusion_type}&location={location}")
    print(k.json())


def get_airport_code(location: str):
    client = genai.Client(api_key=l['gemini'])
    while True:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"give the airport code for the most major airport near this location and nothing else: {location}",
                config={
                    'response_mime_type': 'text/plain',
                }
            )
            return str(response.text)
        except Exception as e:
            print(f"Error generating itinerary: {e}")
            continue

def get_long_lat(location: str):
    client = genai.Client(api_key=l['gemini'])
    while True:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"give me the longitude and latitude of this area and nothing else: {location}",
                config={
                    'response_mime_type': 'application/json',
                    'temperature': 0.2
                }
            )
            return json.loads(str(response.text))
        except Exception as e:
            print(f"Error generating itinerary: {e}")
            continue



#find_local_spots("Seattle", "coffee")


