from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=120)
    datetime = models.DateTimeField()
    seats = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Booking(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guestevent')
    tickets = models.PositiveIntegerField()

    def __str__(self):
        return self.event.title


class UserProfile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
