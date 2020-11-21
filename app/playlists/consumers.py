import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Comment
from .css_colors import CSS_COLORS, colors_amount
from datetime import datetime


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        playlist = text_data_json['playlist']
        user = text_data_json['user']
        user_name = text_data_json['user_name']
        # print(text_data_json['message'], text_data_json['user'], text_data_json['playlist'])
        try:
            Comment.objects.create(
                playlist_id=playlist,
                author_id=user,
                comment=message,
                date=datetime.now()
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_name': user_name,
                    'date': str(datetime.now().strftime("%I:%M %P")),
                    'color': CSS_COLORS[int(user)*3 % colors_amount],
                }
            )
        except:
            pass


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user_name = event['user_name']
        color = event['color']
        date = event['date']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user_name': user_name,
            'color': color,
            'date': date,
        }))