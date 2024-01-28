from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()
from django_editorjs import EditorJsField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class Activity(models.Model):

    datetime = models.DateTimeField(default=timezone.now)

    # can be Post, Comment, Reaction, User
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Activity{self.id}> {self.content_object}"


class Post(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title =  models.CharField(max_length=40, null=False)
    category = models.CharField(max_length=40, null=True, blank=True)
    caption = models.CharField(max_length=100, null=True, blank=True)
    content_img = models.ImageField(upload_to="post_pics", null=False, default='post_default.ico')
    content = EditorJsField(editorjs_config={
        "tools": {
            "Link":{
                    "config":{
                        "endpoint":
                            'http://localhost:8000/api/linkfetching/'
                        }
                },
            "Image":{
                "config": {
                    "endpoints": {
                        "byFile": 'http://127.0.0.1:8000/api/fileUPload/',
                        "byUrl": 'http://localhost:8000/api/fileUPload/',
                    },
                    "additionalRequestHeaders": [{"Content-Type":'multipart/form-data'}]
                }
            },
            "Attaches":{
                    "config":{
                        "endpoint":'http://127.0.0.1:8000/api/fileUPload/'
                    }
                }
        }
    })
    hashtags = models.CharField(max_length=200, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    draft = models.BooleanField(default=True)

    # generic related fields for reverse quering
    activity = GenericRelation(Activity, related_query_name='post_object')

    def __str__(self):
        return f"Post{self.id}__by {self.user.user_name}__('{self.title}', '{self.date_posted}')"


class Comment(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE,
                    related_name='comments')
    parent_comment = models.ForeignKey('self', null=True, blank=True,
                    on_delete=models.CASCADE, related_name='child_comments')
    content = models.TextField(null=False)
    date_posted = models.DateTimeField(null=False, default=timezone.now)

    # generic related fields for reverse quering
    activity = GenericRelation(Activity, related_query_name='comment_object')

    def __str__(self):
        return f"Comment{self.id}('{self.user.user_name}', '{self.content}')"


class Reaction(models.Model):
    emoji = models.CharField(max_length=20)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    # generic relationship fields -- can react on post, comment, etc
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # generic related fields for reverse quering
    activity = GenericRelation(Activity, related_query_name='reaction_object')


    def __str__(self):
        return f"Reaction{self.id}: {self.emoji} | Object: {self.content_object} | User:{self.user.user_name}"


class Following(models.Model):

    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    # generic related fields for reverse quering
    activity = GenericRelation(Activity, related_query_name='following_object')

    def __str__(self):
        return f"Following{self.id}: {self.follower} -> {self.following}"
        
        
class Notification(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=100)
    is_seen = models.BooleanField(default=False)
    event_url = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Notification{self.id} | {self.user.user_name}: {self.message}"
        