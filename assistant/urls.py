from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.open, name="home"),
    path('open/', views.open, name="open"),
    path('register_event/', views.registerEvent, name="eventRegister"),
    path('delete_event/<int:id>/', views.deleteEvent, name="eventDelete"),
    path('edit_event/<int:id>/', views.editEvent, name="eventEdit"),
    path('info_event/<int:id>/', views.eventInfo, name="eventInfo"),
    path('post_tweet/<int:event_id>/', views.tweetPost, name="tweetPost"),
    path('post_tweet_unknownevent/', views.tweetPostUnknownEvent, name="tweetPostUnknownEvent"),
    path('FeSNS/home/', views.fesnsHome, name="FeSNS"),
    path('FeSNS/like/<int:tweet_id>/', views.like_tweet, name="Like"),
    path('register_user/', views.registerUser, name="userRegister"),
    path('login/', views.loginUser, name="login")
]