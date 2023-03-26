from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        username = self.scope['url_route']['kwargs']['user_name']
        print(f'socket: {username} connected')


        await self.accept()