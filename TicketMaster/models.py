from django.db import models
from django.utils import timezone


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100, default="")
    image_url = models.URLField(blank=True, null=True)
    date_time = models.DateTimeField(default=timezone.now)
    venue = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=100, blank=True, null=True)
    tickets_url = models.URLField(blank=True, null=True)
    external_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name