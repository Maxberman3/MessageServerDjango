from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    subject = models.CharField(blank=True, max_length=240)
    creation_date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
