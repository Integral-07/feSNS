from django.db import models

class User(models.Model):

    name = models.CharField(max_length=10)
    mail = models.EmailField(max_length=200)
    

    def __str__(self):

        return '<User : id = ' + str(self.id) + ', ' + self.name + '[ ' + self.mail + ' ]>'

class Event(models.Model):

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    date = models.DateField(max_length=100)
    summary = models.CharField(max_length=2000)
    details = models.TextField(max_length=5000)

    def __str__(self):

        return '<Event : id = ' + str(self.id) + ', ' + self.name + '( ' + self.location + ' : ' + str(self.date) + ' )  | ' + self.summary + '| ' + self.details +  '>'
    
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
