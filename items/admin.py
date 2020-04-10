from django.contrib import admin

from .models import Item, Like


class ItemAdmin(admin.ModelAdmin):
    pass


class LikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Item, ItemAdmin)
admin.site.register(Like, LikeAdmin)
