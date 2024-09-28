from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Room(models.Model):
    roomid = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=50)
    online_users = models.ManyToManyField(User, blank=True)

    def get_online_count(self):
        return self.online_users.count()

    def join_user(self, user):
        self.online_users.add(user)
        self.save()

    def leave_user(self, user):
        self.online_users.remove(user)
        self.save()

    def __str__(self) -> str:
        return self.room_name


class Message(models.Model):
    msgid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room')
    msg = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.room.room_name}__{self.user.username}'
    

class PrivateRoom(models.Model):
    prid = models.AutoField(primary_key=True)
    username_string = models.CharField(max_length=1000)
    private_room_name = models.CharField(max_length=1000 , blank=True)

    def save(self, *args, **kwargs):
        if not self.private_room_name:  
            usernames = self.username_string.split(',')
            self.private_room_name = '_'.join(usernames) + '_private_room'
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.username_string
