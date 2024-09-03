import json

from carpeCalendar.models import Event, EventDates, Category, Place

content = json.load(open("results.json"))

other_location = Place(name="Autre")
other_location.save()

jean_vilar = Place(name="Théâtre Jean Vilar")
jean_vilar.save()

theatre_blocry = Place(name="Théâtre Blocry")
theatre_blocry.save()

placet = Place(name="Salle Placet")
placet.save()

for event in content:
    if Category.objects.filter(name=event["infos"]["category"]).exists():
        category = Category.objects.get(name=event["infos"]["category"])
    else:
        category = Category(name=event["infos"]["category"])
        category.save()

    if Place.objects.filter(name=event["infos"]["place"]).exists():
        location = Place.objects.get(name=event["infos"]["place"])
    else:
        location = other_location

    event_obj = Event(
        title=event["name"],
        description=event["description"],
        location=event["infos"]["place"],
        saved_location=location,
        category=category,
    )

    event_obj.save()

    for date in event["dates"]:
        event_obj.eventdates_set.create(
            start=date[0] + "+02:00",
            end=date[1] + "+02:00",
        )
    event_obj.save()
