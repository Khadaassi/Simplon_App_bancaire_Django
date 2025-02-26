from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)
    
    def __str__(self):
        return f"{self.sender.username if self.sender else 'Anonyme'}: {self.content}"
