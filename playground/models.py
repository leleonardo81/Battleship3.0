from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE ,related_name='user')
    room = models.IntegerField(blank=True, null=True)

    def set_room(self, room_id):
        self.room = int(room_id)
    
    def __str__(self):
        return str(self.user.username)

class Room(models.Model):
    game_start = models.BooleanField(default=False)
    game_finished = models.BooleanField(default=False)
    turn = models.IntegerField(blank=True, null=True)

    def start(self):
        self.game_start = True

    def finish(self):
        self.turn = 0
        self.game_finished = True
    
    def reset(self):
        self.game_finished = False
        self.game_start = False

    def __str__(self):
        return str(self.id)

class Warzone(models.Model):
    player = models.ForeignKey(Player, default=None, on_delete=models.CASCADE ,related_name='player') 
    room = models.IntegerField()
    ship1 = models.CharField(max_length=20, blank=True, null=True)
    ship2 = models.CharField(max_length=17, blank=True, null=True)
    ship3 = models.CharField(max_length=14, blank=True, null=True)
    ship4 = models.CharField(max_length=11, blank=True, null=True)
    shooted = models.CharField(max_length=250, default="")

    def setShip(self, ship_data):
        self.ship1 = ship_data['ship1']
        self.ship2 = ship_data['ship2']
        self.ship3 = ship_data['ship3']
        self.ship4 = ship_data['ship4']
    
    def checkLose(self):
        for sh in self.ship1.split('-')[1:]:
            if sh not in self.shooted.split('-'):
                return False
        for sh in self.ship2.split('-')[1:]:
            if sh not in self.shooted.split('-'):
                return False
        for sh in self.ship3.split('-')[1:]:
            if sh not in self.shooted.split('-'):
                return False
        for sh in self.ship4.split('-')[1:]:
            if sh not in self.shooted.split('-'):
                return False
        return True

    def __str__(self):
        return "{}-{}".format(str(self.player),str(self.room))





