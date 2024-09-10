from django import forms
from .models import Event

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'location', 'date', 'summary']

class EventRegisterForm(forms.Form):

    name = forms.CharField(label='Event Name', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    location = forms.CharField(label='Location', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    date = forms.DateField(label='Date', required=True,widget=forms.DateInput(attrs={'placeholder':"YYYY-MM-DD", 'class':'form-control'}))
    summary = forms.CharField(label='Summary', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

class EventFilterForm(forms.Form):

    name = forms.CharField(label="Event Name(completely match only)")
    location = forms.CharField(label="Location")
    date = forms.DateField(label="Date")