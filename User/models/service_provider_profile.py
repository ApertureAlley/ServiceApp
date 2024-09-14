from django.db import models
from .custom_user import CustomUser

class ServiceProviderProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField()
    skills = models.TextField(max_length=255)
    experience = models.TextField()
    per_hour_rate = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='provider_images/', null=True, blank=True)
    rating = models.PositiveIntegerField(default=0)
    has_kit = models.BooleanField(default=False)
    long_term_contracts = models.BooleanField(default=False)
    short_term_contracts = models.BooleanField(default=False)

    # def __str__(self):
    #     return f"{self.user.username} - ServiceProvider"
