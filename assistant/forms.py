from django import forms
from .models import Event, Tweet

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'location', 'start_date', 'end_date', 'summary', 'details']

class EventRegisterForm(forms.Form):

    name = forms.CharField(label='イベント名', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    location = forms.CharField(label='開催地', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    start_date = forms.DateTimeField(label='開催日', required=True,widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder':"YYYY-MM-DD", 'class':'form-control'}))
    end_date = forms.DateTimeField(label='終了日', required=True,widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder':"YYYY-MM-DD", 'class':'form-control'}))
    summary = forms.CharField(label='概要', required=True, widget=forms.Textarea(attrs={'rows': 5, 'class':'form-control'}))

class EventFilterForm(forms.Form):

    name = forms.CharField(label="イベント名", required=False)
    location = forms.CharField(label="開催地", required=False)
    start_date = forms.DateTimeField(label="開催日", required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control'}))
    end_date = forms.DateTimeField(label="終了日", required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control'}))

class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ['msg']
        widgets = {
            'msg': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': '投稿内容を入力してください'}),
        }