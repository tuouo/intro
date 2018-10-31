from django.contrib import admin

from blog.models import Article, Category, Tag
from comments.models import Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'create_at', 'modify_at')
    # inlines = [CommentInline]


admin.site.register(Category)
admin.site.register(Tag)

