from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=120)
    datetime = models.DateTimeField()
    seats = models.PositiveIntegerField()

    def __str__(self):
        return self.title
