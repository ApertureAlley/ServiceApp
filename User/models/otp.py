from django.db import models

class Otp(models.Model):
  email = models.EmailField(null=False)
  code =  models.CharField(max_length=10)