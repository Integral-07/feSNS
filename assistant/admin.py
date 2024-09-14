from django.contrib import admin
from .models import Event, Store, Tweet, Like

admin.site.register(Tweet)

admin.site.register(Event)

admin.site.register(Like)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'event')
    list_filter = ('event',)