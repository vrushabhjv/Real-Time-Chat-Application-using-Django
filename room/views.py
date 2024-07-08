from django.shortcuts import render
from .models import Room, ChatMessage
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
# the @login_required decorator will ensure that only authenticated users can access the view below this particular decorator. 
# If a user is not authenticated, they will be redirected to the login page. 
# This is useful for ensuring that only authenticated users can access certain pages.
def rooms(request):
    rooms= Room.objects.all()
    
    return render(request,'room/rooms.html', {"rooms":rooms})

@login_required 
def room(request, slug):
    room = Room.objects.get(slug=slug)
    # chatmessages = ChatMessage.objects.filter(room=room).order_by('-date_added')[0:25][::-1] #Same result as below query
    chatmessages = room.messages.all().order_by('-date_added')[0:25][::-1] # This also works because using relation manager as in ChatMessage model, 'room' is a foreign key and for that foreign key related_name = 'messages'.
    # In Django, related_name is an attribute that can be used to specify the name of the reverse relation from the related model back to the model that defines the relation. It is used to specify the name of the attribute that will be used to access the related model from the reverse side of the relation.
    # This attribute is particularly useful when working with many-to-many and foreign key relationships.
    
    print(chatmessages)
    
    return render(request, 'room/room.html', {'room':room, 'chatmessages':chatmessages})