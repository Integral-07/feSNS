from django import forms
from .models import Event, Tweet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'location', 'start_date', 'end_date', 'summary', 'details']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })

class EventRegisterForm(forms.Form):

    name = forms.CharField(label='イベント名', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    location = forms.CharField(label='開催地', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    start_date = forms.DateTimeField(label='開催日', required=True,widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder':"YYYY-MM-DD", 'class':'form-control'}))
    end_date = forms.DateTimeField(label='終了日', required=True,widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder':"YYYY-MM-DD", 'class':'form-control'}))
    summary = forms.CharField(label='概要', required=True, widget=forms.Textarea(attrs={'rows': 5, 'class':'form-control'}))
    details = forms.CharField(label='詳細', required=True, widget=forms.Textarea(attrs={'rows': 10, 'class':'form-control'}))

class EventFilterForm(forms.Form):

    name = forms.CharField(label="イベント名", required=False)
    location = forms.CharField(label="開催地", required=False)
    start_date = forms.DateTimeField(label="開催日", required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control'}))
    end_date = forms.DateTimeField(label="終了日", required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control'}))

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['msg']
        labels = {
            'msg':"",
        }
        widgets = {
            'msg': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'placeholder': '投稿内容を入力',
                'class': 'form-control tweet-textarea',  # 追加: カスタムクラスを適用
                'style': 'border-radius: 10px; border: 2px solid #ff6347;',  # 丸角とボーダー
            }),
        }

    def __init__(self, *args, **kwargs):
        super(TweetForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })

class TweetUnknownEventForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['event', 'msg']
        labels = {
            'event': "",
            'msg': "",
        }
        widgets = {
            'msg': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'placeholder': '投稿内容を入力',
                'class': 'form-control tweet-textarea',
                'style': 'border-radius: 10px; border: 2px solid #ff6347;',  # 丸角とボーダー
            }),
        }

    def __init__(self, *args, **kwargs):
        super(TweetUnknownEventForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })
    
    # フォームの初期化メソッドでイベント選択フィールドを作成
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control event-select',
            'style': 'border-radius: 10px; border: 2px solid #ff6347;',  # 丸角とボーダー
        }),
        empty_label="イベントを選択", 
    )