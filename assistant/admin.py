from django.contrib import admin
from .models import User, Event, Store, Tweet

admin.site.register(User)
admin.site.register(Tweet)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'event')
    list_filter = ('event',)