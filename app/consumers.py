import json
import torch
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from .models import ChatRoom, Message

# Load model and tokenizer once
tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
model = GPT2LMHeadModel.from_pretrained('distilgpt2')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handles incoming messages"""
        data = json.loads(text_data)
        message_content = data['message']
        user = self.scope['user']

        # Save message
        room = await sync_to_async(ChatRoom.objects.get)(id=self.room_id)
        await sync_to_async(Message.objects.create)(
            sender=user,
            chat_room=room,
            content=message_content
        )

        # Broadcast message to all users in the chat
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'username': user.username
            }
        )

    async def chat_message(self, event):
        """Handles broadcasting messages and sending suggestions to the recipient."""
        sender_username = event['username']
        message_content = event['message']
        user = self.scope['user']

        # Don't send suggestions to the sender, only to the receiver(s)
        if user.username != sender_username:
            suggestions = await sync_to_async(self.generate_suggestions)(message_content)
            await self.send(text_data=json.dumps({
                'type': 'suggestions',
                'suggestions': suggestions
            }))

        # Send message to all
        await self.send(text_data=json.dumps(event))

    def generate_suggestions(self, input_text):
        """Generates suggested words based on the received message."""
        try:
            inputs = tokenizer.encode(input_text, return_tensors='pt')
            with torch.no_grad():
                outputs = model(inputs)

            next_token_logits = outputs.logits[:, -1, :]
            probabilities = torch.nn.functional.softmax(next_token_logits, dim=-1)
            top_tokens = torch.topk(probabilities, 5, dim=-1).indices[0].tolist()

            suggestions = []
            for token in top_tokens:
                word = tokenizer.decode([token]).strip()
                if word and word not in ['', '.', ',', '!', '?']:
                    suggestions.append(word)

            return list(dict.fromkeys(suggestions))[:3]  # Remove duplicates and limit to 3 words
        except:
            return []
