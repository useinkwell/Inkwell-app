from django.shortcuts import render, redirect
import json
from django.conf import settings

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
from rest_framework import generics
from rest_framework import mixins


# authentication
from django.contrib.auth import authenticate, login

# permissions
from rest_framework.permissions import IsAuthenticated

# jwt authentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


class PostList(mixins.ListModelMixin, mixins.CreateModelMixin,
                                                generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        data = {
            "title": self.request.POST.get("title"),
            "content": self.request.POST.get("content"),
            "user": self.request.user
        }

        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            # create a post instance using the data
            post = Post(**data)
            post.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     
class PostDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    
class Membership(APIView):          

     def get(self, request):
        
        user = request.user
        serializer = UserSerializer(user)
        data = serializer.data
        
        response_data = {
            'membership': data['membership']
        }

        return Response(response_data)
 

class MembershipForUsername(APIView):          

     def get(self, request, pk):
        
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        data = serializer.data

        response_data = {
            'email': data['email'],
            'usename': data['user_name'],            
            'membership': data['membership']
        }

        return Response(response_data)


class AccountInfo(APIView):

    def get(self, request):

        user = request.user
        serializer = UserSerializer(user)
        data = serializer.data
        response_data = {
            'id': data['id'],
            'usename': data['user_name'],
            'email': data['email'],
            'membership': data['membership'],
            'image_file': data['image_file'],
            'api_token': data['api_token']
        }
        return Response(response_data)


class AccountInfoForUsername(APIView):

    def api_key_is_valid(self, key):
        return User.objects.get(api_token=key)

    def get(self, request, api_key, username):

        user = User.objects.get(user_name=username)

        if user and self.api_key_is_valid(api_key):
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


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.POST)
        data = {}

        if serializer.is_valid():
            new_user = serializer.save()

            # generate jwt access tokens for the new user
            refresh_instance = RefreshToken.for_user(new_user)
            tokens = {
                'refresh_token': str(refresh_instance),
                'access_token': str(refresh_instance.access_token)
            }

            data['response'] = 'Registration Successful'
            data['user_name'] = new_user.user_name
            data['email'] = new_user.email
            data['tokens'] = tokens

            return Response(data, status=status.HTTP_201_CREATED)

        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
