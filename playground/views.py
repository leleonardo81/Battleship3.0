from django.shortcuts import render, redirect
from .models import Room, Player, Warzone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
import json



@login_required(login_url="/login/")
def index(request):
    return render(request, 'playground/index.html')

def room(request, room_id):
    User = Player.objects.get(user=request.user)
    myWarzone = Warzone.objects.get(player=User, room=room_id)
    room = Room.objects.get(id=room_id)
    preparation = not(room.game_start or room.game_finished)
    if User.room == room_id:
        return render(request, 'playground/room.html', {
            'room_id_json': mark_safe(json.dumps(room_id)),
            'my_ship1': check_ship(myWarzone.ship1),
            'my_ship2': check_ship(myWarzone.ship2),
            'my_ship3': check_ship(myWarzone.ship3),
            'my_ship4': check_ship(myWarzone.ship4)
            })
    return redirect('playground:index')

def check_ship(ship):
    if ship == None:
        return 'undefined' 
    elif ship[0]=='v':
        return 'v'+ship.split('-')[1]
    elif ship[0]=='h':
        return 'h'+ship.split('-')[1]
    else:
        return 'undefined'

def join(request):
    if request.method == 'POST':
        User = Player.objects.get(user=request.user)
        room_id = request.POST.get('room')
        try:
            now_room = Room.objects.get(id=room_id)
            if User.room == now_room.id:
                return redirect('playground:room', room_id=room_id)
            elif now_room.game_start:
                return redirect('playground:index')
            else:
                try:
                    Warzone.objects.get(player=User, room=room_id)
                    User.set_room(room_id)
                    User.save()
                    return redirect('playground:room', room_id=room_id)
                except ObjectDoesNotExist:
                    User.set_room(room_id)
                    User.save()
                    Warzone.objects.create(
                        player = User,
                        room = room_id,
                    )
                    return redirect('playground:room', room_id=room_id)
        except ObjectDoesNotExist:
            return redirect('playground:index')
    User = Player.objects.get(user=request.user)
    room_id = User.room
    return redirect('playground:room', room_id=room_id)
    

def create(request):
    User = Player.objects.get(user=request.user)
    Room.objects.create()
    room = Room.objects.last()
    User.set_room(room.id)
    User.save()
    Warzone.objects.create(
        player = User,
        room = room.id
    )
    return redirect('playground:join')
