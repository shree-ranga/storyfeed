from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


# Through table for followers in profile
class Follow(models.Model):
    following_user = models.ForeignKey(
        "Profile", related_name="follower_user", on_delete=models.CASCADE
    )
    follower_user = models.ForeignKey(
        "Profile", related_name="following_user", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.follower_user} following {self.following_user}"
