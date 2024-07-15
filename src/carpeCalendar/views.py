from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Q

from carpeCalendar.models import Event, EventDates

def calendar(request):
    categories = Event.objects.values('category').distinct()
    return render(request, 'calendar.html', {'categories': categories})

def events(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    dates_lst = list(EventDates.objects.filter(Q(Q(start__range=[start, end]) | Q(end__range=[start, end]) | Q(start__lte=start, end__gte=end)), event__validated=True).select_related("event"))

    events_lst = []
    for date in dates_lst:
        events_lst.append(model_to_dict(date.event) | {"start": date.start, "end": date.end})
    return JsonResponse(events_lst, safe=False)

def event(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'event.html', {'event': event})

def add_event_page(request):
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_time = request.POST.get('start')
        end_time = request.POST.get('end')
        location = request.POST.get('location')
        category = request.POST.get('category')
        event = Event(title=title, description=description, location=location, category=category)
        event.save()
        date = EventDates(event=event, start=start_time, end=end_time)
        date.save()
        return redirect("/calendar")

    categories = Event.objects.values('category').distinct()
    return render(request, 'add_event.html', {'categories': categories})