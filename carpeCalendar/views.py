import datetime
import zoneinfo

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
    end_dt = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
    start_dt = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
    if (end_dt - start_dt).days > 90:
        return JsonResponse([], safe=False)
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

def create_qr_code(request):
    return render(request, 'create_qr_code.html')

def add_event_page(request):
    categories = list(Category.objects.values_list('name', flat=True))
    if request.method == 'POST':
        data = request.POST
        starts = data.getlist('start')
        ends = data.getlist('end')
        form = EventForm(data)
        if not form.is_valid():
            return render(request, 'add_event.html', {'status': 'error', 'messages': form.errors, 'categories': categories, "initial": data})
        try:
            location = form.cleaned_data['location']
            category = form.cleaned_data['category']
            event = Event(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                organizer=form.cleaned_data['organizer'],
                location=form.cleaned_data['location'],
                category=Category.objects.get(name=category),
                facebook_link=form.cleaned_data["facebook_link"],
                email_organizer=form.cleaned_data["email_organizer"],
                form_link=form.cleaned_data["form_link"],
                pmr_friendly=form.cleaned_data["pmr_friendly"],
                deaf_friendly=form.cleaned_data["deaf_friendly"],
                blind_friendly=form.cleaned_data["blind_friendly"],
                neurodiversity_friendly=form.cleaned_data["neurodiversity_friendly"],
                granz_filled=form.cleaned_data["granz_filled"],
            )
            event.saved_location = Place.objects.get(name=location) if Place.objects.filter(name=location).exists() else Place.objects.get(name='Autre')
            event.save()
            for start_time, end_time in zip(starts, ends):
                start_datetime = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M').replace(tzinfo=zoneinfo.ZoneInfo('Europe/Brussels'))
                end_datetime = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M').replace(tzinfo=zoneinfo.ZoneInfo('Europe/Brussels'))
                date = EventDates(event=event, start=start_datetime, end=end_datetime)
                date.save()


        except Exception as e:
            print(e)
            return render(request, 'add_event.html', {'status': 'error', 'categories': categories})
        return render(request, 'add_event.html', {'status': 'success', 'categories': categories, **model_to_dict(event)})

    form = EventForm()
    date_form = DateForm()
    return render(request, 'add_event.html', {'categories': categories, 'form': form, 'date_form': date_form})