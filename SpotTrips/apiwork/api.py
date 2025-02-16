import requests
import dotenv


l = dotenv.dotenv_values('.env')


def find_flights(departure, destination, departure_date, arrival_date):
    k = requests.get(f"https://serpapi.com/search.json?engine=google_flights&departure_id={departure}&arrival_id={destination}&gl=us&hl=en&currency=USD&outbound_date={departure_date}&return_date={arrival_date}&api_key={l['api']}")
    print(k.json())

def find_hotels(location, from_date, to_date, max_price):
    k = requests.get(f"https://serpapi.com/search.json?engine=google_hotels&q={location}&gl=us&hl=en&currency=USD&check_in_date={from_date}&check_out_date={to_date}&sort_by=8&min_price=50&max_price={max_price}&rating=8&api_key={l['api']}")
    print(k.json())

def find_local_spots(location, excusion_type):
    k = requests.get(f"https://serpapi.com/search.json?engine=google_local&q={excusion_type}&location={location}")
    print(k.json())



#find_local_spots("Seattle", "coffee")


