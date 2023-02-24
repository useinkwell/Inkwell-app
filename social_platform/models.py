from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    title =  models.CharField(max_length=40, null=False)
    category = models.CharField(max_length=40, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField(null=False)
    content_img = models.ImageField(upload_to="post_pics", null=False, default='post_default.ico')
    hashtags = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    body = models.TextField(null=False)
    date_posted = models.DateTimeField(null=False, default=timezone.now)

    def __str__(self):
        return f"Comment('{self.user.user_name}', '{self.body}')"
        