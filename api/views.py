from django.shortcuts import render

# models
from .serializers import Post, User

# serializers
from .serializers import PostSerializer, UserSerializer

# response / status
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# class-based API views
from rest_framework.views import APIView


class PostList(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

     
class PostDetail(APIView):

     def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class UserMembership(APIView):          

     def get(self, request, pk=None):

        # specific user
        if pk:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response({'membership':serializer.data['membership']})
        
        # current logged-in user
        else:
            pass
               