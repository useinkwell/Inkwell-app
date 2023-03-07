from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()
from django_editorjs import EditorJsField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):
    title =  models.CharField(max_length=40, null=False)
    category = models.CharField(max_length=40, null=True, blank=True)
    caption = models.CharField(max_length=100, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    content = EditorJsField ()
    content_img = models.ImageField(upload_to="post_pics", null=False, default='post_default.ico')
    hashtags = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post__by {self.user.user_name}__('{self.title}', '{self.date_posted}')"


class Comment(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE,
                    related_name='comments')
    parent_comment = models.ForeignKey('self', null=True, blank=True,
                    on_delete=models.CASCADE, related_name='child_comments')
    content = models.TextField(null=False)
    date_posted = models.DateTimeField(null=False, default=timezone.now)

    def __str__(self):
        return f"Comment('{self.user.user_name}', '{self.content}')"


class Reaction(models.Model):
    emoji = models.CharField(max_length=20)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    # generic relationship fields -- can react on post, comment, etc
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    def __str__(self):
        return f"Reaction: {self.emoji} | Object: {self.content_object} | User:{self.user.user_name}"


class Activity(models.Model):

    datetime = models.DateTimeField(default=timezone.now)

    # can be Post, Comment, Reaction, User
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    