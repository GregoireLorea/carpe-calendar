from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Q

from carpeCalendar.models import Event, EventDates, Category, Place
from carpeCalendar.forms import EventForm, DateForm

def home(request):
    return redirect('calendar')

def calendar(request):
    places = Place.objects.all()
    categories = Category.objects.all()
    return render(request, 'calendar.html', {'categories': categories, 'places': places})

def events(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    dates_lst = list(EventDates.objects.filter(Q(Q(start__range=[start, end]) | Q(end__range=[start, end]) | Q(start__lte=start, end__gte=end)), event__validated=True).select_related('event', 'event__category', 'event__saved_location'))
    events_lst = []
    for date in dates_lst:
        events_lst.append(model_to_dict(date.event) | {'start': date.start, 'end': date.end, 'category': model_to_dict(date.event.category), 'saved_location': model_to_dict(date.event.saved_location)})
    return JsonResponse(events_lst, safe=False)

def event(request, event_id):
    event = Event.objects.get(id=event_id)
    if event.validated == False:
        return render(request, 'event.html', {'status': 403})
    dates = EventDates.objects.filter(event=event)
    return render(request, 'event.html', {'event': event, 'dates': dates})

def add_event_page(request):
    categories = list(Category.objects.values_list('name', flat=True))
    if request.method == 'POST':
        data = request.POST
        starts = data.getlist('start')
        ends = data.getlist('end')
        form = EventForm(data)
        if not form.is_valid():
            return render(request, 'add_event.html', {'status': 'error', 'categories': categories, "initial": data})
        try:
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            location = form.cleaned_data['location']
            category = form.cleaned_data['category']
            organizer = form.cleaned_data['organizer']
            event = Event(title=title, description=description, organizer=organizer, location=location, category=Category.objects.get(name=category))
            event.saved_location = Place.objects.get(name=location) if Place.objects.filter(name=location).exists() else Place.objects.get(name='Autre')
            event.save()
            for start_time, end_time in zip(starts, ends):
                date = EventDates(event=event, start=start_time, end=end_time)
                date.save()


        except Exception as e:
            print(e)
            return render(request, 'add_event.html', {'status': 'error', 'categories': categories})
        return render(request, 'add_event.html', {'status': 'success', 'categories': categories})

    form = EventForm()
    date_form = DateForm()
    return render(request, 'add_event.html', {'categories': categories, 'form': form, 'date_form': date_form})