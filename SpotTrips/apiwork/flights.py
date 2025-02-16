import requests
import json

def create_offer_request(origin, destination, departure_date, arrival_date, user_info):
    url = "https://api.duffel.com/air/offer_requests?return_offers=true&supplier_timeout=10000"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": "Bearer <YOUR_ACCESS_TOKEN>"
    }
        # Example usage:
    fare_info = [
        
    ]
    for l in user_info.keys():
        for j in range(user_info[l]):
            fare_info.append({"type": user_info[l]})
    data = {
        "data": {
            "slices": [
                {
                    "origin": origin,
                    "destination": destination,
                    "departure_time": {
                        "to": "17:00",
                        "from": "09:45"
                    },
                    "departure_date": departure_date,
                    "arrival_date": arrival_date,
                    "arrival_time": {
                        "to": "17:00",
                        "from": "09:45"
                    }
                }
            ],
            "passengers": user_info,
            "max_connections": 0,
            "cabin_class": "economy"
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()




