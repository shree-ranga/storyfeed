from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings

from notifications.models import Notification


class User(AbstractUser):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    is_private = models.BooleanField(default=False)
    report_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE
    )
    bio = models.CharField(max_length=150, null=True, blank=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", through="Follow"
    )
    all_likes = models.IntegerField(default=0)
    blocked_profiles = models.ManyToManyField(
        settings.AUTH_USER_MODEL, symmetrical=False, related_name="blocked_by"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .tasks import process_avatar_image

        process_avatar_image.delay(self.user.id)

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

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


class ProfileAvatar(models.Model):
    profile = models.OneToOneField(Profile, primary_key=True, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="profileImages")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .tasks import process_avatar_image

        process_avatar_image.delay(self.profile.user.id)

    @property
    def avatar_url(self):
        try:
            return self.avatar.url
        except:
            return None

    def __str__(self):
        return f"{self.avatar.name} {self.profile.user.username}"
