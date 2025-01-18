from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)  # Mark message as deleted (for admin use)

    def __str__(self):
        return f'{self.user.username} - {self.content[:20]}'
