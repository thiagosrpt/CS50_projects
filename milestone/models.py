from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from rest_framework import serializers


# Create your models here.

class User(AbstractUser):
    pass

class Event(models.Model):
    name = models.CharField(max_length = 255)
    organizer = models.ForeignKey("User", on_delete=models.CASCADE, null=True, default=None, blank=True)
    participants = models.ManyToManyField("User", related_name='paticipants', blank=True)
    delivery = models.BooleanField(default=False)
    pickup = models.BooleanField(default=False)
    dinein = models.BooleanField(default=False)
    date = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    

    def serialize(self):

        return {
            "id": self.id,
            "name": self.name,
            "organizer": self.organizer.username,
            "organizer_lastname": self.organizer.last_name,
            "organizer_name": self.organizer.first_name,
            "participants": [user.username for user in self.participants.all()],
            "participants_lastname": [user.last_name for user in self.participants.all()],
            "participants_name": [user.first_name for user in self.participants.all()],
            "delivery": self.delivery,
            "pickup": self.pickup,
            "dinein": self.dinein,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": Like.objects.filter(event=self.id, like=True).count()
        }

class Like(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, null=True, default=None, blank=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True, default=None, blank=True)
    food = models.ForeignKey("Food", on_delete=models.CASCADE, null=True, default=None, blank=True)
    like = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "event_id": self.event.id,
            "event_name": self.event.name,
            "user_id": self.user.id,
            "username": self.user.username,
            "food_id": self.food.id,
            "food_name": self.food.name,
            "like": self.like,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class LikeSerializer(serializers.ModelSerializer):

  total_likes = serializers.SerializerMethodField()
  
  def get_total_likes(self, obj):
        try:
            return obj.total_likes
        except:
            return None

class Food(models.Model):
    name = models.CharField(max_length = 255)
    delivery = models.BooleanField(default=False)
    pickup = models.BooleanField(default=False)
    dinein = models.BooleanField(default=False)
    distance = models.FloatField(max_length = 4)
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = models.FloatField(max_length = 3, default=None)
    site = models.CharField(max_length = 255, default=None)
    image_url = models.CharField(max_length = 1024, null=True, default=None, blank=True)
    description = models.CharField(max_length = 512, null=True, default=None, blank=True)


    def serialize(self):
        return {
            "id": self.id,
            "delivery": self.delivery,
            "pickup": self.pickup,
            "dinein": self.dinein,
            "distance": self.distance,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "ratings": self.ratings,
            "site": self.site,

        }