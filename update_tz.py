import zoneinfo
import datetime

from carpeCalendar.models import EventDates, Event

for event in Event.objects.all().order_by('-created_at'):
    if event.created_at < datetime.datetime(2024, 9, 19, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo('Europe/Brussels')):
        break
    for date in event.eventdates_set.all():
        date.start = date.start.replace(tzinfo=zoneinfo.ZoneInfo('Europe/Brussels'))
        date.end = date.end.replace(tzinfo=zoneinfo.ZoneInfo('Europe/Brussels'))

        date.save()