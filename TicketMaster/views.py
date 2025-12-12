from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from .forms import EventForm
from .models import Event

# Create your views here.
def index(request):
    if request.method == "POST":
        genreInput = request.POST['genre-input']
        locationInput = request.POST['location-input']

        if not genreInput:
            messages.info(request, "Search term cannot be empty. Please enter a search term")
            return redirect('index')
        if not locationInput:
            messages.info(request, "City cannot be empty. Please enter a city")
            return redirect('index')

        events = get_events(genreInput, locationInput, country_code='US', apikey='YGGgx0CLSlCN96D8iKHhfDoKcKAX4K18')
        if events is None:
            messages.info(request, "Sorry... No results were found for the entered search term and city.")
            return redirect('index')
        else:
            #print(events)
            event_listings = events['_embedded']['events']
            list_of_events = []

            for event in event_listings:
                event_name = event['name']
                event_image = event['images'][0]['url']
                event_date_time = event.get("dates", {}).get('start', {}).get('dateTime', {})

                #date_object = datetime.strptime(event_date_time[:20], '%Y-%m-%dT%H:%M')
                #event_date_time = date_object.strftime('%m/%d/%y %H:%M')

                venue = event['_embedded']['venues'][0]['name']
                print(event['_embedded']['venues'][0])
                city = event['_embedded']['venues'][0]['city']['name']
                state = event['_embedded']['venues'][0]['state']['name']
                address = event['_embedded']['venues'][0]['address']['line1']
                tickets = event['url']
                event_id = event['id']

                event_details = {
                    'event_name': event_name,
                    'event_image': event_image,
                    'event_date_time': event_date_time,
                    'event_venue': venue,
                    'event_city': city,
                    'event_state': state,
                    'event_address': address,
                    'event_tickets': tickets,
                    'event_id': event_id
                }
                list_of_events.append(event_details)

            context = {'event_listings': list_of_events}
            return render(request, 'index.html', context)

    return render(request, 'index.html')

def get_events(genreInput, locationInput, country_code, apikey):
    try:
       url = "https://app.ticketmaster.com/discovery/v2/events.json"

       #url:`https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US&classificationName=${genreInput}&city=${locationInput}&sort=date,asc&apikey=YGGgx0CLSlCN96D8iKHhfDoKcKAX4K18`,

       params = {
           "classificationName": genreInput,
           "city": locationInput,
           "countryCode": country_code,
           "apikey": apikey,
           "sort": "date,asc"
       }

       response = requests.get(url, params=params)
       response.raise_for_status()
       data = response.json()
       return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def beta(request):
    return render(request, 'beta/beta.html')

#CRUD Create
def list_add(request):
    if request.method == "POST":
        event_name = request.POST['event-name']
        event_image = request.POST['event-image']
        event_venue = request.POST['event-venue']
        event_city = request.POST['event-city']
        event_state = request.POST['event-state']
        event_address = request.POST['event-address']
        event_tickets = request.POST['event-tickets']
        # event_id = request.POST['event-id']
        Event.objects.create(name=event_name, image_url=event_image, venue=event_venue, city=event_city, state=event_state, address=event_address, tickets_url=event_tickets)
    return redirect('list_save')

#CRUD Read
def list_save(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'saved-list.html', context)

#CRUD Update
# Update a save boolean that turns on or off based on if user clicks and the current saved value
def list_update(request, id):
    event = Event.objects.get(id=id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list_save')
    context = {'form': form}
    return render(request, 'update-list.html', context)

#CRUD Delete
def list_delete(request, id ):
    event = Event.objects.get(id=id)
    if request.method == "POST":
        event.delete()
        return redirect('list_save')
    context = {'event': event}
    return render(request, 'delete-confirm.html', context)

