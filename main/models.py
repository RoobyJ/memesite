from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    class Meta:
        ordering = ['-id']
    post_title = models.CharField(max_length=75, unique=True)
    post_content = models.TextField(blank=True, default='')
    post_image = models.ImageField(upload_to='pics')
    post_published = models.DateTimeField('date published', auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('main:post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.comment_author.username}'
