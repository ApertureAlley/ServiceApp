from  django.db import models
from  .custom_user import CustomUser
class BusinessOwnerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    business_type = models.CharField(max_length=20, choices=[("Individual", "Individual"), ("Agency", "Agency"), ("Business", "Business")], blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def _str_(self):
        return self.company_name