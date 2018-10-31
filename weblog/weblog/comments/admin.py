from django.contrib import admin
from comments.models import Comment

@admin.register(Comment)
class CommentAdimn(admin.ModelAdmin):
    list_display = ('name', 'email', 'url', 'text', 'create_at', 'modify_at')

