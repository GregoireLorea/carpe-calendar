from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Event
from .models import EventDates
from .models import Category
from .models import Place

class EventAdmin(ModelAdmin):
    list_display = ['title', 'validation_status', 'location', 'organizer', 'category', 'get_dates', 'created_at']
    list_filter = ["validated", "category", "created_at", "updated_at"]
    search_fields = ["title", "location"]
    actions = ["validate_selected_events", "invalidate_selected_events"]
    list_per_page = 10
    
    # Configuration des champs dans le formulaire de détail
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'description', 'category', 'organizer')
        }),
        ('Localisation', {
            'fields': ('location', 'saved_location')
        }),
        ('Contact', {
            'fields': ('email_organizer', 'facebook_link', 'form_link')
        }),
        ('Accessibilité', {
            'fields': ('pmr_friendly', 'deaf_friendly', 'blind_friendly', 'neurodiversity_friendly')
        }),
        ('Granz', {
            'fields': ('granz_filled', 'granz_validated')
        }),
        ('Validation', {
            'fields': ('validated',),
            'classes': ('wide',),
            'description': 'Cochez cette case pour valider cet événement et le rendre visible dans le calendrier.'
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']

    def validation_status(self, obj):
        """Affiche clairement le statut de validation"""
        # Rafraîchir l'objet depuis la DB pour éviter les problèmes de cache
        obj.refresh_from_db()
        
        if obj.validated:
            return "✅ VALIDÉ"
        else:
            return "❌ NON VALIDÉ"
    
    validation_status.short_description = "Statut de validation"
    validation_status.admin_order_field = "validated"
    validation_status.boolean = True  # Permet le tri par boolean

    @admin.action(description="✅ Valider les événements sélectionnés")
    def validate_selected_events(self, request, queryset):
        count = queryset.update(validated=True)
        self.message_user(request, f"{count} événement(s) validé(s) avec succès.")

    @admin.action(description="❌ Invalider les événements sélectionnés")
    def invalidate_selected_events(self, request, queryset):
        count = queryset.update(validated=False)
        self.message_user(request, f"{count} événement(s) invalidé(s) avec succès.")

    def get_dates(self, obj):
        return "|\n".join([str(date) for date in obj.eventdates_set.all()])

class EventDatesAdmin(ModelAdmin):
    list_display = ['event', 'start', 'end']
    list_filter = ['event']
    search_fields = ['event']
    list_editable = ['start', 'end']


class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'parent']
    list_filter = ['parent']
    list_editable = ['parent']

class PlaceAdmin(ModelAdmin):
    list_display = ['name', 'address', 'latitude', 'longitude']
    list_editable = ['address', 'latitude', 'longitude']

admin.site.register(Event, EventAdmin)
admin.site.register(EventDates, EventDatesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Place, PlaceAdmin)
