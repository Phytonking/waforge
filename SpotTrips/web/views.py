from datetime import timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from apiwork import location, api, itinerary
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
        iten = itinerary.get_travel_itinerary(location.get_random_travel_destination_name(), itinerary.days_of_travel_calc(from_date, to_date), depart_from=travel_from, budget=budget)
        itener = Itenerary(id=uuid.uuid4(), json=iten)
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
        return render(request, "web/iten.html", {"iten": xt})

def book_iten(request, id):
    





