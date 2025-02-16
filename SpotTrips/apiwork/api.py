import json
import os
from google import genai
from apiwork.location import get_random_travel_destination_name
from datetime import datetime
import requests
import dotenv


l = dotenv.dotenv_values('.env')

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
            import time
            time.sleep(0.5)
            continue


def find_flights(departure, destination, departure_date, arrival_date):
    k = requests.get(f"https://serpapi.com/search.json?engine=google_flights&departure_id={departure}&arrival_id={destination}&gl=us&hl=en&currency=USD&outbound_date={departure_date}&return_date={arrival_date}&api_key={l['api']}")
    departure = k.json()['best_flights'][0]
    print(departure["departure_token"])
    xdep = get_airport_code(departure)
    xout = get_airport_code(destination)
    print(xdep, xout)
    a = requests.get(f"https://serpapi.com/search.json?engine=google_flights&departure_id={xdep}&arrival_id={xout}&gl=us&hl=en&currency=USD&outbound_date={departure_date}&return_date={arrival_date}&departure_token={departure['departure_token']}&api_key={l['api']}")
    print(a.json())
    #https://serpapi.com/search.json?engine=google_flights&departure_id=CDG&arrival_id=AUS&gl=us&hl=en&currency=USD&outbound_date=2025-02-17&return_date=2025-02-23&departure_token=WyJDalJJYjJkT2VVNDVPVTVJWjBsQlJtaE9RM2RDUnkwdExTMHRMUzB0TFhaMGRYVXlOa0ZCUVVGQlIyVjVWMlJ2UTBGNlYwOUJFZ3BWUVRVMmZGVkJOamMyR2dzSXphOElFQUlhQTFWVFJEZ2NjTTJ2Q0E9PSIsW1siQ0RHIiwiMjAyNS0wMi0xNyIsIkVXUiIsbnVsbCwiVUEiLCI1NiJdLFsiRVdSIiwiMjAyNS0wMi0xNyIsIkFVUyIsbnVsbCwiVUEiLCI2NzYiXV1d&api_key=d4059b69d5bfec93e6c7b05b0fb1b530ee6d60fb44361bcaaa62d87bf136c757
    arrvial = None
    try:
        arrvial = a.json()['best_flights'][0]
    except Exception as e:
        arrival = {"error": "no return flight found, reload page. "}
    print(departure, arrvial)
    return [departure, arrvial]

def find_hotels(location, from_date, to_date, max_price):
    k = requests.get(f"https://serpapi.com/search.json?engine=google_hotels&q={location} hotels&gl=us&hl=en&currency=USD&check_in_date={from_date}&check_out_date={to_date}&sort_by=8&min_price=50&max_price={max_price}&rating=8&api_key={l['api']}")
    return k.json()['properties'][0]

def find_local_spots(location, excusion_type):
    k = requests.get(f"https://serpapi.com/search.json?engine=google_local&q={excusion_type}&location={location}")
    print(k.json())




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
            import time
            time.sleep(0.5)
            continue


def get_first_images(keywords):
    if not (3 <= len(keywords) <= 5):
        raise ValueError("Please provide between 3 to 5 keywords.")
    
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": l["pexels"]}
    images = []
    
    for keyword in keywords:
        params = {"query": keyword, "per_page": 1}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data["photos"]:
                images.append(data["photos"][0]["src"]["original"])
            else:
                images.append(None)  # No image found for this keyword
        else:
            images.append(None)  # Error in fetching results
    
    return images

keywords = ["travel", "nature", "city"]  # Modify this list
first_images = get_first_images(keywords)



#find_local_spots("Seattle", "coffee")


