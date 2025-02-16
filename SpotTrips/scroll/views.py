from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
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

from flask import redirect
from scroll.utils import *
# Create your views here.

def index(request):
    return render(request, "scroll/index.html")

@csrf_exempt  # Disable CSRF protection for simplicity (use proper authentication in production)
def travel_posts_api(request):
    if request.method == "GET":
        try:
            travelpost = make_new_post()
            return JsonResponse(json.loads(travelpost), status=200, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def trip_to_blank(request, location):
    request.session['destination'] = location
    return redirect("web:index")
