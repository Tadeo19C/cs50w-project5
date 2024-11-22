from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils import timezone
from channels.db import database_sync_to_async

class AudioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"audio_{self.room_name}"
        self.participants = set()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        user = self.scope['user']
        if user.is_authenticated:
            self.participants.add(user.username)
            await self.update_participants()

    async def disconnect(self, close_code):
        user = self.scope['user']
        if user.is_authenticated and user.username in self.participants:
            self.participants.remove(user.username)
            await self.update_participants()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_participants(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return list(User.objects.filter(username__in=self.participants).values('id', 'username', 'first_name', 'last_name'))

    async def update_participants(self):
        participants = await self.get_participants()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'participant_update',
                'participants': participants
            }
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', None)
        action = text_data_json.get('action', None)

        if action == "audio_toggle":
            user = self.scope['user']
            mic_status = text_data_json.get('mic_status', False)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'mic_status_update',
                    'user': user.username,
                    'mic_status': mic_status
                }
            )
        elif action == "start_call":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'call_started',
                    'user': self.scope['user'].username
                }
            )
        elif action == "end_call":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'call_ended',
                    'user': self.scope['user'].username
                }
            )
        elif message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.scope['user'].username
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'user': event['user']
        }))

    async def participant_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'participant_update',
            'participants': event['participants']
        }))

    async def mic_status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'mic_status_update',
            'user': event['user'],
            'mic_status': event['mic_status']
        }))

    async def call_started(self, event):
        await self.send(text_data=json.dumps({
            'type': 'call_started',
            'user': event['user']
        }))

    async def call_ended(self, event):
        await self.send(text_data=json.dumps({
            'type': 'call_ended',
            'user': event['user']
        }))
