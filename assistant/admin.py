from django.contrib import admin
from .models import User, Event
from rangefilter.filters import DateRangeFilter

admin.site.register(User)
admin.site.register(Event)

'''
class EventAdmin(admin.ModelAdmin):
    list_display = ('access_date_time', 'request_url', 'request_method',)
    list_filter = (('access_date_time', DateRangeFilter),) #フィルター機能を利用するフィールドの指定

admin.site.register(Event, EventAdmin)
'''