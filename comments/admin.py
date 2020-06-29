from django.contrib import admin

from .models import Comment, CommentLike


class CommentAdmin(admin.ModelAdmin):
    pass


class CommentLikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
