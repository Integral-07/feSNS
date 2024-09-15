from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Event, Tweet, Like
from .forms import EventRegisterForm, EventFilterForm, EventForm, TweetForm, TweetUnknownEventForm
import json
from django.db.models import Q
from datetime import datetime


def index(request):

    params = {

        'title' : 'Assistant/Index',
        'msg' : 'This page is under construction.Please, check me later.'
    }

    return render(request, 'assistant/index.html', params)

def home(request):

    return render(request, 'assistant/home.html')


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
@login_required(login_url="/assistant/login/")
def registerEvent(request):

    params = {

        'title' : 'イベント登録',
        'message' : 'Fill in bellow blanks to register events',
        'form' : EventRegisterForm(),
        'search_form' : EventFilterForm(),
    }
    if(request.method == "POST"):
        
        obj = Event(owner=request.user)
        event = EventForm(request.POST, instance=obj)
        event.save()

        return redirect(to="/assistant/open/")
    
    return render(request, 'assistant/eventRegister.html', params)


@login_required(login_url="/assistant/login/")
def editEvent(request, id):

    obj = Event.objects.get(id=id)
    if(request.method == 'POST'):
        event = EventForm(request.POST, instance=obj)
        event.save()
        return redirect(to="/assistant/open/")

    params = {

        'title' : 'イベント情報編集',
        'id' : id,
        'form' : EventForm(instance=obj),
    }

    return render(request, 'assistant/eventEdit.html', params)

@login_required(login_url="/assistant/login/")
def deleteEvent(request, id):

    event = Event.objects.get(id=id)
    if(request.method == 'POST'):
        event.delete()
        return redirect(to="/assistant/open/")
    
    params = {

        'title' : 'イベント情報削除',
        'id' : id,
        'obj' : event,
    }

    return render(request, 'assistant/eventDelete.html', params)

def eventInfo(request, id):

    event = Event.objects.get(id=id)
    stores = event.stores.all()
    tweets = event.tweets.all()
    user = request.user

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
        'user' : user,
        'stores': stores,
        'tweets': tweets,
        'stores_json': json.dumps(stores_data),  # JSON形式でデータを渡す
    }

    return render(request, 'assistant/eventInfo.html', params)


@login_required(login_url="/assistant/login/")
def tweetPost(request, event_id):
    
    event = Event.objects.get(id=event_id)
    user = request.user

    params = {

        'title' : 'Tweet',
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


@login_required(login_url="/assistant/login/")
def tweetPostUnknownEvent(request):
    
    user = request.user

    params = {

        'title' : 'Tweet',
        'msg' : 'Try tweet to fill in flollowing form!',
        'user_data' : user,
        'form': TweetUnknownEventForm(),
    }

    if(request.method == "POST"):

        #form = TweetUnknownEventForm(request.POST)
        obj = Tweet(user=user, good_count=0)
        tweet = TweetUnknownEventForm(request.POST, instance=obj)
        tweet.save()
        return redirect(to="/assistant/FeSNS/home/")


    return render(request, 'assistant/tweetPostUnknownEvent.html', params)


@login_required(login_url="/assistant/login/")
def like_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    user = request.user

    # ユーザーがこのツイートに「いいね」していないか確認
    like = Like.objects.filter(user=user, tweet=tweet).first()
    if not like:
        # 新しい「いいね」を作成
        Like.objects.create(user=user, tweet=tweet)
        tweet.good_count += 1
        tweet.save()

    else:

        like.delete()
        tweet.good_count -= 1
        tweet.save()
    
    return redirect(to="/assistant/FeSNS/home")


def fesnsHome(request):

    tweets = Tweet.objects.all()
    events = Event.objects.all()
    params = {

        'title' : 'FeSNS',
        'tweets' : tweets,
        'events' : events
    }

    return render(request, 'assistant/FeSNS.html', params)


def registerUser(request):

    if(request.method == 'POST'):
        form = UserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()
            login(request, user)

            return redirect(to="/assistant/open/")

    else:
        form = UserCreationForm()

    params = {

        'title' : 'ユーザ登録',
        'form' : form,
    }

    return render(request, 'assistant/userRegister.html', params)

def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(to="/assistant/open/")  # ログイン後のリダイレクト先
    else:
        form = AuthenticationForm()

    params = {
        
        'form': form,
    }

    return render(request, 'assistant/login.html', params)

@login_required(login_url="/assistant/login/")
def addStore(request, event_id):

    params = {

        'title': '出店情報',
        'msg':'<p>This page is under construction. Please check me later.</p>'
    }

    return render(request, 'assistant/addStore.html', params)

@login_required(login_url="/assistant/login/")
def showUser(request):

    user = request.user

    params = {

        'title': 'ユーザ情報',
        'user': user,
    }

    return render(request, 'assistant/showUser.html', params)