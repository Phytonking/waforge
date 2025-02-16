import requests
import json
import dotenv

config = dotenv.dotenv_values('.env')

def create_offer_request(origin, destination, departure_date, arrival_date, user_info):
    url = "https://api.duffel.com/air/offer_requests?return_offers=true&supplier_timeout=10000"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {config['duffel']}"
    }
        # Example usage:
    fare_info = [
        
    ]
    for l in user_info.keys():
        for j in range(int(user_info[l])):
            fare_info.append({"type": l})
    data = {
        "data": {
            "slices": [
                {
                    "origin": origin,
                    "destination": destination,
                    #"departure_time": {
                    #    "to": "17:00",
                    #    "from": "09:45"
                    #},
                    "departure_date": str(departure_date),
                    "arrival_date": str(arrival_date),
                    #"arrival_time": {
                    #    "to": "17:00",
                    #    "from": "09:45"
                    #}
                }
            ],
            "passengers": fare_info,
            "max_connections": 1,
            "cabin_class": "economy"
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()




