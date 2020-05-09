from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {'fields': ["post_title", "post_published"]}),
        ("Content", {"fields": ["post_content"]}),
        ("Image", {"fields": ["post_image"]}),
        ("Created_by", {"fields": ["created_by"]})
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('comment_author', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
