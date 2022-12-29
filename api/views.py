from django.shortcuts import render

from django.http import JsonResponse
from user.models import Post
from .serializers import PostSerializer


def posts_list(request):    
     # get all the posts from database
    posts = Post.objects.all()

    # serialize them to json
    serializer = PostSerializer(posts, many=True)

    # return json
    return JsonResponse({"posts": serializer.data})
