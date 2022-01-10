from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', related_name='userFollowers', symmetrical=False, blank=True)
    following = models.ManyToManyField('self', related_name='userFollowing', symmetrical=False, blank=True)
    posts = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, default=None, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "followers":  [user.username for user in self.followers.all()],
            "following": [user.username for user in self.following.all()],
            "posts": self.posts
        }

class Post(models.Model):
    creator = models.ForeignKey("User", on_delete=models.CASCADE, null=True, default=None, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    text_content = models.CharField(max_length = 1000)
    likes = models.ManyToManyField("User", related_name='userLikes', blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "postedOn": self.date.strftime("%b %d %Y, %I:%M %p"),
            "textContent": self.text_content,
            "likeCount": self.likes.count(),
            "likes": self.likes
        }
