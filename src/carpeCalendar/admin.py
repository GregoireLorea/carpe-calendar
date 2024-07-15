from django.contrib import admin

from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'category', 'validated']
    list_editable = ["validated"]
    list_filter = ["validated", "category"]
    search_fields = ["title", "location"]
    actions = ["validate_selected_events", "invalidate_selected_events"]

    @admin.action(description="Validate selected events")
    def validate_selected_events(self, request, queryset):
        queryset.update(validated=True)

    @admin.action(description="Invalidate selected events")
    def invalidate_selected_events(self, request, queryset):
        queryset.update(validated=False)

admin.site.register(Event, EventAdmin)
