import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatMessage, Room
from django.contrib.auth.models import User
from html import escape

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] # get the room name from the url route
        self.room_group_name = 'chat_%s' % self.room_name # create a group name for the room
        print(f"From ChatConsumer: Connecting to room: {self.room_name}")

        # join the room group
        # The group is created on the first group_add call and users are added to it. Subsequent users joining the same room are added to the same group.
        await self.channel_layer.group_add( # add the current webSocket connection to the group
            self.room_group_name, # group name
            self.channel_name # Current webSocket connection is represented by channel_name, automatically assigned by django channels 
        )
        print("Accepting connect requests")
        await self.accept() # Formally accepts the WebSocket connection. Until this method is called, the connection is not fully established, and the client cannot send or receive messages.

    async def disconnect(self, close_code): # disconnect the user
        print("Disconnecting from room")
        # leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Disconnected from room : {self.room_group_name}")
        
    # The receive() function is the main entry point for handling incoming WebSocket messages in the 'ChatConsumer' class. It is responsible for processing the client's message, storing it in the database, and then broadcasting it to all other clients in the same room.
    async def receive(self, text_data):
        data = json.loads(text_data) # Parse the JSON data from the WebSocket message
        message = data['message']
        username = data['username']
        room = data['room']
        
        await self.save_message(username, room, message) # Save the message to the database
        
        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,  # The group name (e.g., 'chat_room1')
            {
                'type': 'chat_message',
                'message':message,
                'username':username,
                'room':room,
            }
        )
        
    # The 'chat_message' method is called when the "type" key in the message dictionary passed to 'group_send' matches the name of the method. This is how the Channels library routes messages within groups to the appropriate consumer methods. 
    # it sends the message to the client
    async def chat_message(self, event):
        message = escape(event['message']) # The 'escape()' function in Python's "html module" is used to convert special characters in a string to their corresponding HTML-safe sequences. This is essential for preventing Cross-Site Scripting (XSS) attacks when displaying user-generated content in web pages. XSS attacks occur when an attacker is able to inject malicious scripts into web pages that are viewed by other users.
        username = escape(event['username'])
        room = event['room']
        
        # Creates a dictionary with the data to send, converts it to JSON string using 'json.dumps()' function. This JSON string is sent to WebSocket client using "self.send()" method
        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'room':room,
        }))
    
    # The 'save_message' method saves the message to the database. This is done asynchronously using "sync_to_async" to ensure it does not block the event loop.    
    @sync_to_async
    def save_message(self, username, room, chatmessage):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        
        # Create a new ChatMessage and save it to the database
        ChatMessage.objects.create(user=user, room=room, content=chatmessage)