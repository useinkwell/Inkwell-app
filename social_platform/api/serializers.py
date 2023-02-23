from rest_framework import serializers

from social_platform.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }
        