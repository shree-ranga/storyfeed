from django.contrib import admin

from .models import User, Profile, Follow, ProfileAvatar


class UserAdmin(admin.ModelAdmin):
    pass


class ProfileAvatarAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


class FollowAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(ProfileAvatar, ProfileAvatarAdmin)
