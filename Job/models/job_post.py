from django.db import models
from User.models.custom_user import CustomUser
from .category import Category

class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirement = models.TextField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    deadline = models.DateField()
