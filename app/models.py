from django.db import models
from django.contrib.auth.models import User

# class Message(models.Model):
#     content = models.TextField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room_name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     deleted = models.BooleanField(default=False)  # Mark message as deleted (for admin use)

#     def __str__(self):
#         return f'{self.user.username} - {self.content[:20]}'


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Optional for group chats
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name="chat_rooms")

    def __str__(self):
        return self.name if self.is_group else f"Private Chat {self.id}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.username} -> {self.chat_room.name if self.chat_room.is_group else "Private Chat"}'


    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.content[:20]}'
