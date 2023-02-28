from rest_framework import serializers

from social_platform.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    
    # only needed if using EditorJsField in the Post model
    content = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }
        