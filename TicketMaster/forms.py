from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'image_url', 'date_time',
            'venue', 'city', 'state',
            'address', 'tickets_url'
        ]