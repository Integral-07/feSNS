from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="index"),
    path('open/', views.open, name="open"),
    path('register_event', views.registerEvent, name="eventRegister"),
    path('delete_event/<int:id>', views.deleteEvent, name="eventDelete"),
    path('edit_event/<int:id>', views.editEvent, name="eventEdit"),
]