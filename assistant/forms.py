from django import forms
from .models import Event, Tweet

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'location', 'date', 'summary', 'details']

class EventRegisterForm(forms.Form):

    name = forms.CharField(label='Event Name', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    location = forms.CharField(label='Location', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    date = forms.DateField(label='Date', required=True,widget=forms.DateInput(attrs={'placeholder':"YYYY-MM-DD", 'class':'form-control'}))
    summary = forms.CharField(label='Summary', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

class EventFilterForm(forms.Form):

    name = forms.CharField(label="Event Name(completely match only)")
    location = forms.CharField(label="Location")
    date = forms.DateField(label="Date")

class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ['msg']
        widgets = {
            'msg': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': '投稿内容を入力してください'}),
        }