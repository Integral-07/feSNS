from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Tweet
from .forms import EventRegisterForm, EventFilterForm, EventForm, TweetForm
import json
from django.db.models import Q
from datetime import datetime


def index(request):

    params = {

        'title' : 'Assistant/Index',
        'msg' : 'This page is under construction.Please, check me later.'
    }

    return render(request, 'assistant/index.html', params)

@login_required(login_url="/admin/login/")
def open(request):
    # 初期データとフォームの準備
    user = request.user
    form = EventFilterForm(request.GET or None)
    events = Event.objects.all()

    # フォームのバリデーションと絞り込み
    if form.is_valid():
        name = form.cleaned_data.get('name')
        location = form.cleaned_data.get('location')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        # 名前で部分一致
        if name:
            events = events.filter(name__icontains=name)

        # 開催地で部分一致
        if location:
            events = events.filter(location__icontains=location)

        # 開催期間で絞り込み
        if start_date and end_date:
            events = events.filter(
                Q(start_date__lte=start_date) & Q(end_date__gte=end_date)
            )
        elif start_date:
            events = events.filter(start_date__gte=start_date)
        elif end_date:
            events = events.filter(end_date__lte=end_date)

    # パラメータの準備
    params = {
        'title': '開催中のイベント',
        'msg': 'festival info',
        'data': events,
        'user': user,
        'form': form,
    }

    return render(request, 'assistant/open.html', params)


#@staff_member_required(login_url="admin/login/")
@login_required(login_url="/admin/login/")
def registerEvent(request):

    params = {

        'title' : 'イベント登録',
        'message' : 'Fill in bellow blanks to register events',
        'form' : EventRegisterForm(),
        'search_form' : EventFilterForm(),
    }
    if(request.method == "POST"):
        
        obj = Event()
        event = EventForm(request.POST, instance=obj)
        event.save()

        return redirect(to="/assistant/open/")
    
    return render(request, 'assistant/eventRegister.html', params)


@login_required(login_url="/admin/login/")
def editEvent(request, id):

    obj = Event.objects.get(id=id)
    if(request.method == 'POST'):
        event = EventForm(request.POST, instance=obj)
        event.save()
        return redirect(to="/assistant/open/")

    params = {

        'title' : 'assistant/eventEdit',
        'id' : id,
        'form' : EventForm(instance=obj),
    }

    return render(request, 'assistant/eventEdit.html', params)

@login_required(login_url="/admin/login/")
def deleteEvent(request, id):

    event = Event.objects.get(id=id)
    if(request.method == 'POST'):
        event.delete()
        return redirect(to="/assistant/open/")
    
    params = {

        'title' : 'assistant/eventDelete',
        'id' : id,
        'obj' : event,
    }

    return render(request, 'assistant/eventDelete.html', params)

@login_required(login_url="/admin/login/")
def eventInfo(request, id):

    event = Event.objects.get(id=id)
    stores = event.stores.all()
    tweets = event.tweets.all()

    stores_data = [
        {
            'name': store.name,
            'latitude': store.latitude,
            'longitude': store.longitude,
            'info_window_content': store.info_window_content
        } for store in stores
    ]

    params = {

        'title': 'イベント情報',
        'message' : 'event infomation',
        'id' : id,
        'obj' : event,
        'stores': stores,
        'tweets': tweets,
        'stores_json': json.dumps(stores_data),  # JSON形式でデータを渡す
    }

    return render(request, 'assistant/eventInfo.html', params)


@login_required(login_url="/admin/login/")
def tweetPost(request, event_id):
    
    event = Event.objects.get(id=event_id)
    user = request.user

    params = {

        'title' : 'Assistant/TweetPost',
        'msg' : 'Try tweet to fill in flollowing form!',
        'event_data' : event,
        'user_data' : user,
        'form': TweetForm(),
    }

    if(request.method == "POST"):
        obj = Tweet(user=user, event=event, good_count=0)
        tweet = TweetForm(request.POST, instance=obj)
        tweet.save()
        return redirect(to="/assistant/FeSNS/home/")


    return render(request, 'assistant/tweetPost.html', params)


def fesnsHome(request):

    tweets = Tweet.objects.all()
    events = Event.objects.all()
    params = {

        'title' : 'FeSNS',
        'tweets' : tweets,
        'events' : events
    }

    return render(request, 'assistant/FeSNS.html', params)
