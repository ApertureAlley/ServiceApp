from django.db import models

class Location(models.Model):
  state = models.CharField(max_length=50, null=True, blank=True)
  city = models.CharField(max_length=50, null=True, blank=True)
