import json



# Function to generate HTML for the itinerary
def generate_itinerary_html(itinerary):
    html_output = ""

    for day_info in itinerary:
        day = day_info["day"]
        travel_day = day_info["travel_day"]
        excursions = day_info["excursions"]
        restaurants = day_info["restaurants"]
        
        # Create a div for each day
        html_output += f'<div class="bg-white p-6 rounded-lg shadow-md border border-orange-200" style="margin-bottom: 20px; padding: 10px;">'
        html_output += f'<h3 class="text-lg font-medium text-orange-700">Day {day}</h3>'
        
        if travel_day:
            html_output += f'<div class="mt-2 text-gray-600"><p><strong>Travel Day</strong></p></div>'
        else:
            # Excursions section
            if excursions:
                html_output += f'<div class="mt-2 text-gray-600">'
                html_output += f'<p><strong>Excursions:</strong></p>'
                html_output += f'<ul>'
                for excursion in excursions:
                    html_output += f'<li>{excursion}</li>'
                html_output += f'</ul>'
                html_output += f'</div>'
            
            # Restaurants section
            if restaurants:
                html_output += f'<div class="mt-2 text-gray-600">'
                html_output += f'<p><strong>Meals:</strong></p>'
                for meal, place in restaurants.items():
                    html_output += f'<p><strong>{meal.capitalize()}:</strong> {place}</p>'
                html_output += f'</div>'
        
        html_output += '</div>'

    return html_output

