from django.shortcuts import render
from .models import Room
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
    
    return render(request, 'room/room.html', {'room':room})