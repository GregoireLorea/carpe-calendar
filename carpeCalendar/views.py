from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Q

from carpeCalendar.models import Event, EventDates, Category, Place
from carpeCalendar.forms import EventForm

def calendar(request):
    places = Place.objects.all()
    categories = Category.objects.all()
    return render(request, 'calendar.html', {'categories': categories, 'places': places})

def events(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    dates_lst = list(EventDates.objects.filter(Q(Q(start__range=[start, end]) | Q(end__range=[start, end]) | Q(start__lte=start, end__gte=end)), event__validated=True).select_related("event", "event__category", "event__saved_location"))
    events_lst = []
    for date in dates_lst:
        events_lst.append(model_to_dict(date.event) | {"start": date.start, "end": date.end, "category": model_to_dict(date.event.category), "saved_location": model_to_dict(date.event.saved_location)})
    return JsonResponse(events_lst, safe=False)

def event(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'event.html', {'event': event})

def add_event_page(request):
    categories = list(Category.objects.values_list('name', flat=True))
    if request.method == 'POST':
        form = EventForm(request.POST)
        if not form.is_valid():
            return render(request, 'add_event.html', {'status': 'error', 'categories': categories})
        try:
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            start_time = form.cleaned_data['start']
            end_time = form.cleaned_data['end']
            location = form.cleaned_data['location']
            category = form.cleaned_data['category']
            event = Event(title=title, description=description, location=location, category=Category.objects.get(name=category))
            event.save()
            date = EventDates(event=event, start=start_time, end=end_time)
            date.save()
        except Exception as e:
            print(e)
            return render(request, 'add_event.html', {'status': 'error', 'categories': categories})
        return render(request, 'add_event.html', {'status': 'success', 'categories': categories})

    form = EventForm()
    return render(request, 'add_event.html', {'categories': categories, 'form': form})