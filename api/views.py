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
               

class AccountDetail(APIView):

    def api_key_is_valid(self, key):
        return User.objects.get(api_token=key)

    def get(self, request, api_key, username):

        if self.api_key_is_valid(api_key):
            user = User.objects.get(user_name=username)
            serializer = UserSerializer(user)
            data = serializer.data
            response_data = {
                'id':data['id'],
                'usename':data['user_name'],
                'email':data['email'],
                'membership':data['membership'],
                'image_file':data['image_file'],
                'api_token':'classified'
            }
            return Response(response_data)


class PostCreate(APIView):
    
    def post(self, request, api_key):

        user = User.objects.get(api_token=api_key)
        if user:
            id = str(user.id)

            data = {
                "title": self.request.GET.get("title"),
                "content": self.request.GET.get("content"),
                "user": id
            }

            serializer = PostSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        