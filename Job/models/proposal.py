from django.db import models
from User.models.custom_user import CustomUser
from .job_post import JobPost

class Proposal(models.Model):
    content = models.TextField()
    job_post_id = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    proposal_rate = models.DecimalField(decimal_places=2,max_digits=10)
    estimated_completion_time = models.DateField()
    additional_note = models.TextField()
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]
    status = models.TextField(choices=STATUS_CHOICES)