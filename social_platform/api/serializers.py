from rest_framework import serializers

from social_platform.models import Post, Comment, Reaction, Notification


class PostSerializer(serializers.ModelSerializer):
    
    # only needed if using EditorJsField in the Post model
    content = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }
        

class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ['emoji', 'user']
        extra_kwargs = {
            'user': {'read_only': True}
        }


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'message': {'read_only': True}
        }
        
        