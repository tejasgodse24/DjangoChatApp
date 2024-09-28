from channels.generic.websocket import WebsocketConsumer
import json 
from asgiref.sync import async_to_sync
from chat.models import *


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(room_name = self.room_name)
        self.user = self.scope['user']
        self.user_inbox = f'{self.user.username}_private_room'

        self.accept()

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        if self.user.is_authenticated:

            async_to_sync(self.channel_layer.group_add)(self.user_inbox, self.channel_name) # join self private room also

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'user_join',
                    'user':self.user.username
                }
            )
            self.room.online_users.add(self.user)
        

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(self.user_inbox, self.channel_name)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'user_leave',
                    'user':self.user.username
                }
            )
            self.room.online_users.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        message = json_data['message']
        print(json_data)

        if not self.user.is_authenticated:
            return 

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message,
                'user': self.user.username
            }
        )
        Message.objects.create(user = self.user, room = self.room, msg = message)

    def chat_message(self, event):
        self.send(text_data = json.dumps(event))

    def user_join(self, event):
        self.send(text_data = json.dumps(event))

    def user_leave(self, event):
        self.send(text_data = json.dumps(event))
