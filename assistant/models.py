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

    def __str__(self):

        return '<Event : id = ' + str(self.id) + ', ' + self.name + '( ' + self.location + ' : ' + self.date + ' )  | ' + self.summary + '>'