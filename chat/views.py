from django.shortcuts import render, redirect
from chat.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.
def index_view(request):
    errmsg = ""
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        user_obj = User.objects.filter(username = username)
        
        if len(user_obj) == 0 :
            user_obj = User.objects.create(username = username)
            user_obj.set_password(password)
            user_obj.save()  
            
        user_obj = authenticate(username = username, password = password)

        if not user_obj :
            return render(request, 'index.html', {'errmsg':"Password is wrong"})
        
        if user_obj : 
            login(request, user_obj)
            return redirect('chat_room', room_name = "-1")

    return render(request, 'index.html', {'errmsg':errmsg})


def room_view(request, room_name):
    errmsg = ""
    if request.method == "POST":
        room_name = request.POST.get('room_name').strip()
        rooms = Room.objects.filter(room_name = room_name)
        if len(rooms) > 0:
            errmsg = "Group already exists"
        else:
            room_obj = Room.objects.create(room_name = room_name)

        return redirect('chat_room', room_name = room_name)
    
    try:
        room = Room.objects.get(room_name = room_name)
        messages = Message.objects.filter(room = room)
    except Exception as e:
        room = None
        messages = None

    all_rooms = Room.objects.all().exclude(room_name__endswith = "_private_room")
    all_users = User.objects.all().exclude(username = request.user.username)
    context = {
        'room' : room,
        'messages': messages,
        'all_rooms' : all_rooms,
        'errmsg' : errmsg,
        'flag': 2,
        'all_users' : all_users
    }
    return render(request, 'room.html', context)

def private_room_view(request, username):
    errmsg = ""
    if username != '-1':
        try:
            user_obj = User.objects.filter(username = username)
            if len(user_obj) > 0:
                private_room = PrivateRoom.objects.get(
                    Q(username_string__contains = username) & 
                    Q(username_string__contains = request.user.username)
                )
            room = Room.objects.get(room_name = private_room.private_room_name)
            messages = Message.objects.filter(room = room)
        except Exception as e:
            private_room = PrivateRoom.objects.create(username_string = f'{username},{request.user.username}')
            room = Room.objects.create(room_name = private_room.private_room_name)
            messages = Message.objects.filter(room = room)

        all_users = User.objects.all().exclude(username = request.user.username)
        user_obj = User.objects.get(username = username)
    else:
        room = None
        messages = None
        all_users = User.objects.all().exclude(username = request.user.username)
        user_obj = None

    context = {
        'room' : room,
        'messages': messages,
        'errmsg' : errmsg,
        'flag': 1,
        'all_users' : all_users,
        'user' : user_obj
    }
    return render(request, 'privateroom.html', context)

# def partial_chatwindow_view(request, room_name):
#     print("success")
#     room = Room.objects.get(room_name = room_name)
#     messages = Message.objects.filter(room = room)
#     context = {
#         'room' : room,
#         'messages': messages
#     }
#     return render(request, 'room.html#film-item', context)
