import requests
import json
import dotenv
import apiwork.api as api
from amadeus import Client, ResponseError, Location, reference_data, shopping, booking

config = dotenv.dotenv_values('.env')

def search_stays(check_in_date, check_out_date, destination):
    url = "https://api.duffel.com/stays/search"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {config['duffel']}"
    }
    data = {
        "data": {
            "rooms": 1,
            "mobile": False,
            "location": {
                "radius": 10,
                "geographic_coordinates": api.get_long_lat(destination)
            }
            },
            "check_out_date": str(check_out_date),
            "check_in_date": str(check_in_date)
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    return response.json()

def search_hotel(check_in_date, check_out_date, city_code, radius=5, radius_unit="KM", chain_codes=None, amenities=None, ratings=None, hotel_source="ALL", ):
    hotel_list = reference_data.Locations.hotels.get(city_code=city_code)
    hotel_offers = []
    hotel_ids = []
    for i in hotel_list.data:
        hotel_ids.append(i['hotelId'])
    num_hotels = 40
    kwargs = {'hotelIds': hotel_ids[0:num_hotels],
        'checkInDate': check_in_date,
        'checkOutDate': check_out_date}
        
    search_hotel = shopping.hotel_offers_search.get(kwargs)
    hotel = None
    for hotel in search_hotel.data:
        offer_availability = shopping.hotel_offer_search(hotel['hotel']['hotelId']).get()
        if offer_availability.status_code == 200:
            hotel = hotel['hotel']['hotelId']
            break
        else:
            continue
    return reference_data.Locations.hotels.by_hotels.get(id=hotel)


def book_hotel(request, offer_id, guests):
        # Confirm availability of a given offer
    offer_availability = shopping.hotel_offer_search(offer_id).get()
    if offer_availability.status_code == 200:
        guests = [
              {
                  "tid": 1,
                  "title": "MR",
                  "firstName": "BOB",
                  "lastName": "SMITH",
                  "phone": "+33679278416",
                  "email": "bob.smith@email.com"
              }
            ]
        travel_agent = {
                    "contact": {
                        "email": "test@test.com"
                    }   
            }
            
        room_associations = [
              {
                  "guestReferences": [
                      {
                          "guestReference": "1"
                      }
                  ],
                  "hotelOfferId": offer_id
              }
          ]

        payment = {
              "method": "CREDIT_CARD",
              "paymentCard": {
                  "paymentCardInfo": {
                      "vendorCode": "VI",
                      "cardNumber": "4151289722471370",
                      "expiryDate": "2030-08",
                      "holderName": "BOB SMITH"
                  }
              }
          }
        book = booking.hotel_bookings.post(
                guests=guests, 
                travel_agent=travel_agent,
                room_associations=room_associations,
                payment=payment).data
        return True
    else:
        return None
