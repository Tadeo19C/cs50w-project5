from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    topic_name = models.CharField(max_length=200)

    def __str__(self):
        return self.topic_name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # One Host Can Create Multiple Rooms -->  One To Many

    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    # One Topic Are Part Of  Multiple Rooms  -->  One To Many 

    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    # One User Can Be Part Of More Than One Rooms
    # One Room Can Have More Then One User
    # Many To Many

    room_name = models.CharField(max_length=200)
    room_description = models.TextField(null=True, blank=True)
    # participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_time', '-created_time']

    def __str__(self):
        return self.room_name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # User Can Send Multiple Message -->  One To Many

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # ['on_delete=models.CASCADE'] Means When Parent(Room) Is deleted, Then All The Child(message) is Deleted 
    # Room Can Have Multiple Message -->  One To Many

    message_body = models.TextField()
    
    updated_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_time', '-created_time']

    def __str__(self):
        return self.message_body[0:50]

