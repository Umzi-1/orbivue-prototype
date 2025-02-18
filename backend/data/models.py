from django.db import models

# Create your models here.
# backend/data/models.py
from django.db import models

class Activity(models.Model):
    machine_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    activity_type = models.CharField(max_length=20)
    window_title = models.TextField()
    metadata = models.JSONField()

class Screenshot(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)