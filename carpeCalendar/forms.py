from django import forms


class EventForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, required=False)
    location = forms.CharField(max_length=200)
    category = forms.CharField(max_length=200)
    organizer = forms.CharField(max_length=200)
    facebook_link = forms.URLField(max_length=500, required=False)
    email_organizer = forms.EmailField(max_length=200, required=False)
    form_link = forms.URLField(max_length=500, required=False)

    pmr_friendly = forms.BooleanField(required=False)
    deaf_friendly = forms.BooleanField(required=False)
    blind_friendly = forms.BooleanField(required=False)
    neurodiversity_friendly = forms.BooleanField(required=False)
    granz_filled = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        facebook_link = cleaned_data.get('facebook_link', '')
        
        # Check if facebook link is an event link
        if facebook_link and not (
            facebook_link.startswith('https://facebook.com') or
            facebook_link.startswith('https://www.facebook.com') or
            facebook_link.startswith('https://m.facebook.com') or
            facebook_link.startswith('facebook.com')
        ):
            raise forms.ValidationError("Facebook link must be an event link")
            
        return cleaned_data


class DateForm(forms.Form):
    start = forms.DateTimeField()
    end = forms.DateTimeField()

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and end and start > end:
            raise forms.ValidationError("End date must be after start date")
            
        return cleaned_data
