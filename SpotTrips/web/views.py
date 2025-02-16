from datetime import timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from apiwork import location, api, itinerary, flights, hotels
import datetime
from web.models import *
import uuid
from django.urls import reverse
from web.utils import *
import json


# Create your views here.
def index(request):
    return render(request, "web/index.html")

def generate_iten(request):
    if request.method == "GET":
        return redirect('web:index')
    elif request.method == "POST":
        from_date = request.POST["departure-date"]
        to_date = request.POST["arrival-date"]
        travel_from = request.POST["departure-area"]
        budget = float(request.POST["budget"])
        iten = str(itinerary.get_travel_itinerary(location.get_random_travel_destination_name(), itinerary.days_of_travel_calc(from_date, to_date), depart_from=travel_from, budget=budget))
        itener = Itenerary(id=uuid.uuid4(), json=iten, from_date=from_date, to_date=to_date, departing_from=travel_from)
        itener.save()
        url = reverse('web:itinerary', kwargs={"id": itener.id})
        return HttpResponseRedirect(url)
        
def open_iten(request, id):
    if request.method == "GET":
        iten = Itenerary.objects.get(id=id)
        xlk = str(iten.json).replace("\'", "\"")
        iten.json = xlk
        iten.save()
        xt = generate_itinerary_html(json.loads(iten.json)["itinerary"])
        return render(request, "web/iten.html", {"iten": xt, "id": iten.id})

def book_iten(request, xid):
    iten = Itenerary.objects.get(id=xid)
    if request.method == "GET":
        #add user information
        return render(request, "web/additional.html", {"id":iten.id, "iten":iten})
    elif request.method == "POST":
        adult = request.POST["adult-tickets"]
        child = request.POST["child-tickets"]
        infant = request.POST["infant-tickets"]
        xlk = str(iten.json).replace("\'", "\"")
        iten.json = xlk
        iten.save()
        #create the flight
        flight = api.find_flights(departure=api.get_airport_code(str(iten.departing_from)), destination=api.get_airport_code(json.loads(iten.json)["destination"]), departure_date=iten.from_date, arrival_date=iten.to_date)
        #create the hotel stay
        hotel = api.find_hotels(from_date=iten.from_date, to_date=iten.to_date, location=api.get_airport_code(json.loads(iten.json)["destination"]), max_price=100)
        return render(request, "web/final_iten.html", {"flights": flight, "hotel": hotel, "iten": iten, "id":iten.id})
        







