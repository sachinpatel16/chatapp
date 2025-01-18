# # consumers.py

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         # Ensure channel_layer is properly initialized
#         if self.channel_layer:
#             # Join room group
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the room group
#         if self.channel_layer:
#             await self.channel_layer.group_discard(
#                 self.room_group_name,
#                 self.channel_name
#             )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))


#v2

# consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth.models import User

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         # Join the room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         username = self.scope['user'].username  # Get the username of the user sending the message

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'username': username  # Include the username with the message
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']  # Get the username of the sender

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username  # Include the username with the message
#         }))


# v3

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import models
from asgiref.sync import sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        username = self.scope['user'].username  # Get the username of the user sending the message

        # Save the message to the database asynchronously
        await self.save_message(message_content, username)

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'username': username
            }
        )

    # Save message to the database asynchronously using sync_to_async
    @sync_to_async
    def save_message(self, message_content, username):
        # Create and save the message to the database
        message = Message.objects.create(
            content=message_content,
            user=self.scope['user'],
            room_name=self.room_name
        )
        return message

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']  # Get the username of the sender

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username  # Include the username with the message
        }))
