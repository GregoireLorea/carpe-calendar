from django.contrib import admin

from .models import Event
from .models import EventDates
from .models import Category
from .models import Place

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'saved_location', 'organizer', 'category', 'validated', 'get_dates', 'form_link', 'facebook_link', 'email_organizer', 'created_at']
    list_editable = ["validated"]
    list_filter = ["validated", "category", "created_at", "updated_at"]
    search_fields = ["title", "location"]
    actions = ["validate_selected_events", "invalidate_selected_events"]
    list_per_page = 10

    @admin.action(description="Validate selected events")
    def validate_selected_events(self, request, queryset):
        queryset.update(validated=True)

    @admin.action(description="Invalidate selected events")
    def invalidate_selected_events(self, request, queryset):
        queryset.update(validated=False)

    def get_dates(self, obj):
        return "|\n".join([str(date) for date in obj.eventdates_set.all()])

class EventDatesAdmin(admin.ModelAdmin):
    list_display = ['event', 'start', 'end']
    list_filter = ['event']
    search_fields = ['event']
    list_editable = ['start', 'end']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_filter = ['parent']
    list_editable = ['parent']

class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'latitude', 'longitude']
    list_editable = ['address', 'latitude', 'longitude']

admin.site.register(Event, EventAdmin)
admin.site.register(EventDates, EventDatesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Place, PlaceAdmin)
