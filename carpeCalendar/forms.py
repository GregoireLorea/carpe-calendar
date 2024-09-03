from django import forms


class EventForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(max_length=200)
    category = forms.CharField(max_length=200)
    organizer = forms.CharField(max_length=200)


class DateForm(forms.Form):
    start = forms.DateTimeField()
    end = forms.DateTimeField()

    def clean(self):
        start = self.cleaned_data['start']
        end = self.cleaned_data['end']

        if start > end:
            raise forms.ValidationError("End date must be after start date")
