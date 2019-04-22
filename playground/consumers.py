from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room, Warzone, Player
from django.contrib.auth.models import User
# from django.core import serializers
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = '%s' % self.room_name

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
    
    def ready(self, data):
        user = User.objects.get(username = data['user'])
        player = Player.objects.get(user = user)
        warzone = Warzone.objects.get(player=player, room = player.room)
        warzone.setShip(data)
        warzone.save()
        self.refresh(data)
    
    def next_turn(self):
        room_id = int(self.room_group_name)
        room = Room.objects.get(id = room_id)
        players = Player.objects.filter(room = room_id)
        players_count = len(players)
        for i in range(players_count-1):
            room.turn = (room.turn+1)%players_count
            room.save()
            if not Warzone.objects.get(player=players[room.turn], room=room_id).checkLose():
                return 0
        room.finish()
        room.save()
            
    def attack(self, data):
        user = User.objects.get(username = data['attacked_player'])
        player = Player.objects.get(user = user)
        warzone = Warzone.objects.get(player=player, room = int(data['room']))
        warzone.shooted+= data['zone_id']+'-'
        warzone.save()
        self.next_turn()
        self.refresh(data)

    def playerSerialzers(self, player, room):
        p_warzone = Warzone.objects.get(player=player, room=room)
        sh1_shooted = []
        sh2_shooted = []
        sh3_shooted = []
        sh4_shooted = []
        shooted = []
        if p_warzone.shooted != None:
            shooted = p_warzone.shooted.split('-')
            for m in p_warzone.shooted.split("-"):
                if m in p_warzone.ship1.split('-'):
                    sh1_shooted.append(m)
                elif m in p_warzone.ship2.split('-'):
                    sh2_shooted.append(m)
                elif m in p_warzone.ship3.split('-'):
                    sh3_shooted.append(m)
                elif m in p_warzone.ship4.split('-'):
                    sh4_shooted.append(m)
            
        return {
            'name':player.user.username,
            'shooted': shooted,
            'sh1_shooted': sh1_shooted,
            'sh2_shooted': sh2_shooted,
            'sh3_shooted': sh3_shooted,
            'sh4_shooted': sh4_shooted,}

    def check_winner(self, room):
        players = Player.objects.filter(room=room)
        for i in range(len(players)):
            if not Warzone.objects.get(player=players[i], room=room).checkLose():
                return i

    def refresh(self, data):
        room = int(self.room_group_name)
        players = Player.objects.filter(room=room)#janlupa disort lah
        players_json = []
        players_mark = []
        now_room = Room.objects.get(id = room)
        if now_room.game_finished:
            game_state = 'finished'
            for p in players:
                players_json.append(self.playerSerialzers(p, room))
            for p in players:   
                players_mark.append(False)
            players_mark[self.check_winner(room)] = True
            
        elif now_room.game_start:
            game_state = 'started'
            for p in players:
                players_json.append(self.playerSerialzers(p, room))
            for p in players:   
                players_mark.append(False)
            players_mark[now_room.turn] = True
        else:
            for p in players:
                players_json.append({'name':p.user.username})
            game_state = 'preparation'
            for p in players:
                if Warzone.objects.get(player=p, room=room).ship4 != None:
                    players_mark.append(True)
                else:
                    players_mark.append(False)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'room_refresh', 
                'players':players_json,
                'players_mark':players_mark,
                'gamestate':game_state,
            }
        )

    def startGame(self, data):
        room_id = int(self.room_group_name)
        room = Room.objects.get(id = room_id)
        ready_to_start = True
        for pleyer in Warzone.objects.filter(room = room_id):
            if pleyer.ship4 == None:
                ready_to_start = False
        if ready_to_start: 
            room.start()
            room.turn = 0
            room.save()
            self.refresh(data)
        

    commands = {
        'refresh':refresh,
        'start' :startGame,
        'ready' :ready,
        'attack':attack,
    }
    # Receive message from WebSocket

    def receive(self, text_data):
        data_json = json.loads(text_data)
        self.commands[data_json['command']](self, data=data_json)

    
    def room_refresh(self, event):
        players = event['players']
        state = event['gamestate']
        mark = event['players_mark']
        self.send(text_data=json.dumps({
            'players': players,
            'players_mark':mark,
            'state' : state,
            'action' : 'refresh'
        }))

        

    # Receive message from room group
    def chat_message(self, event):
        message = event['players']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))