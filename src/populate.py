import json

from carpeCalendar.models import Event

content = json.load(open("../results.json"))

for event in content:
    event_obj = Event(
        title=event["name"],
        description=event["description"],
        location=event["infos"]["place"],
        category=event["infos"]["category"],
    )

    event_obj.save()

    for date in event["dates"]:
        event_obj.eventdates_set.create(
            start=date[0] + "+02:00",
            end=date[1] + "+02:00",
        )
    event_obj.save()
