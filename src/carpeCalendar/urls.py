from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.calendar, name='calendar'),
    path('event/<int:event_id>/', views.event, name='event'),
    path('events/', views.events, name='events'),
    path('add-event', views.add_event_page, name='add_event'),
]
