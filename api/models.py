from django.db import models
# from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.content

    def comments(self):
        try:
            comments = self.comments.all().order_by('-timestamp')
        except:
            comments = None
        return comments

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.author.username + self.post.content