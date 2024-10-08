from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200)
    saved_location = models.ForeignKey('Place', on_delete=models.CASCADE, null=True, blank=True)
    email_organizer = models.EmailField(max_length=200, blank=True, null=True)
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    form_link = models.URLField(max_length=200, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    organizer = models.CharField(max_length=200, default="Non renseigné")
    pmr_friendly = models.BooleanField(default=False)
    deaf_friendly = models.BooleanField(default=False)
    blind_friendly = models.BooleanField(default=False)
    neurodiversity_friendly = models.BooleanField(default=False)
    granz_filled = models.BooleanField(default=False)
    granz_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    validated = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class EventDates(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.start) + " - " + str(self.end)

class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name