import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] # get the room name from the url route
        self.room_group_name = 'chat_%s' % self.room_name # create a group name for the room

        # join the room group
        
        await self.channel_layer.group_add( # add the user to the group
            self.room_group_name, # group name
            self.channel_name # channel name 
        )
        
        await self.accept() # accept the connection

    async def disconnect(self): # disconnect the user
        # leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        