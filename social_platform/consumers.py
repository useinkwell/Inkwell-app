from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
import json

from user.models import User
from social_platform.models import Notification


class ClientConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_name = self.scope['url_route']['kwargs']['user_name']

        print(f'socket: {user_name} connected')

        # store channel_name in session to be accessible from views
        self.scope['session']['channel_name'] = self.channel_name

        # add consumer instance to personal user_name group (e.g user_mary)
        await self.channel_layer.group_add(f'user_{user_name}', self.channel_name)

        # add consumer instance to all groups representing followers of other users
        # (e.g follows_rihanna, follows_poppy, etc)
        await self.add_channel_to_group_for_each_followed_user(user_name)

        await self.accept()

    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        print(f'\n\nFROM CLIENT: {message}\n\n')

    
    async def client_sender(self, event):
        '''just for testing client communication'''

        print(f'\n\nCLIENT SENDER IS RUNNING\n\n')
        message = event['message']

        await self.send(text_data=json.dumps(
            {
                'message': message
            }
        ))


    async def notification(self, event):
        print(f'\nNOTIFICATION IS RUNNING\n\n')
        message = event['message']
        action = event['action']
        action_id = event['action_id']
        by = event['by']
        action_content = event.get('action_content')
        receiver = event.get('receiver')
        receiver_id = event.get('receiver_id')
        
        sender = await sync_to_async(User.objects.get)(user_name=by)


        # create notification instance for all concerned users

        @sync_to_async
        def create_post_notification_instances():
            '''creates a notification instance for each follower'''
            followers_object = sender.followers.all()
            followers = map(lambda follower_instance: \
            follower_instance.follower, followers_object)
            notifications = [Notification(
                    message=message,
                    user=follower
                    ) for follower in followers]
            Notification.objects.bulk_create(notifications)

        
        @sync_to_async
        def create_following_notification_instance():
            '''creates a notification instance for the followed user'''
            user_name = self.scope['url_route']['kwargs']['user_name']
            user = User.objects.get(user_name=user_name)
            Notification.objects.create(
                user=user,
                message=message
            )

        
        @sync_to_async
        def create_reaction_notification_instance():
            '''creates a notification instance for content creator of the
            object reacted on'''
            user_name = self.scope['url_route']['kwargs']['user_name']
            user = User.objects.get(user_name=user_name)
            Notification.objects.create(
                user=user,
                message=message
            )

        
        @sync_to_async
        def create_comment_notification_instance():
            '''creates a notification instance for user who posted or commented,
            when the post is commented on or the comment is replied to'''

            user_name = self.scope['url_route']['kwargs']['user_name']
            user = User.objects.get(user_name=user_name)
            Notification.objects.create(
                user=user,
                message=message
            )


        if action == 'post':
            await create_post_notification_instances()

        elif action == 'following':
            await create_following_notification_instance()

        elif action == 'reaction':
            await create_reaction_notification_instance()

        elif action == 'comment':
            await create_comment_notification_instance()
        

        # send notification to client via websocket
        await self.send(text_data=json.dumps(
            {
                'message': message,
                'action': action,
                'action_id': action_id,
                'by': by
            }
        ))    

    
    @sync_to_async
    def add_channel_to_group_for_each_followed_user(self, user_name:str):
        user = User.objects.get(user_name=user_name)
        generator_for_user_names_of_followed_users = \
            (name for name in map(lambda following_instance:\
                following_instance.following.user_name, user.following.all()))

        for name in generator_for_user_names_of_followed_users:

            print(f'\nadding channel name to follower group for {name}\n')

            async_to_sync(self.channel_layer.group_add)(
                f'follows_{name}',
                self.channel_name
            )