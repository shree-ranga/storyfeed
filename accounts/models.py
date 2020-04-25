from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings

from notifications.models import Notification


class User(AbstractUser):
    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE
    )
    avatar = models.ImageField(null=True, blank=True)
    bio = models.CharField(max_length=150, null=True, blank=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", through="Follow"
    )
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def avatar_url(self):
        try:
            return self.avatar.url
        except:
            return None

    def __str__(self):
        return f"{self.user.username}'s profile"


# Through table for followers in profile
class Follow(models.Model):
    following_user = models.ForeignKey(
        Profile, related_name="follower_user", on_delete=models.CASCADE
    )
    follower_user = models.ForeignKey(
        Profile, related_name="following_user", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notifications = GenericRelation(Notification)

    class Meta:
        unique_together = ("following_user", "follower_user")

    def __str__(self):
        return f"{self.follower_user} is following {self.following_user}"
