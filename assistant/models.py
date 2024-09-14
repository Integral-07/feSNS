from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    start_date = models.DateTimeField(max_length=100)
    end_date = models.DateTimeField(max_length=100)
    summary = models.CharField(max_length=2000)
    details = models.TextField(max_length=5000)
    owner = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)

    def __str__(self):

        return '<Event : id = ' + str(self.id) + ', ' + self.name + '( ' + self.location + \
              ' : ' + str(self.start_date) + ' - ' + str(self.end_date) + ' )  | ' \
                + self.summary + '| ' + self.details + ' by ' + str(self.owner) +'>'
    
class Store(models.Model):

    event = models.ForeignKey(Event, related_name='stores', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    info_window_content = models.TextField(max_length=1000)

    def __str__(self):
        return self.name
    
class Tweet(models.Model):

    event = models.ForeignKey(Event, related_name='tweets', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    msg = models.TextField(max_length=2000)
    good_count = models.IntegerField(default=0)
    pub_day = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<Tweet ID: " + str(self.id) + "(pub-day " + str(self.pub_day) + " ) [ " + self.msg + " ] by " + str(self.user) + " GOOD( " + str(self.good_count) + " )>"
