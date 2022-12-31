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

# authentication
from django.contrib.auth import authenticate, login


class PostList(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

     
class SpecificPost(APIView):

     def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


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


class LoginView(APIView):
    def post(self, request):

        # first try to get login details from the query params (/?email=)
        data = request.GET
        if not data:
            # otherwise get login from the request body
            data = json.loads(request.body)

        email = data['email']
        password = data['password']
 
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
 
        if user is not None:

            login(request=request, user=user)
 
            # Return the token as part of the response
            return redirect(settings.LOGIN_REDIRECT_URL)
 
        else:
            # Return a response indicating that the login failed
            return Response({"login": "failed"})


class LoginSuccess(APIView):

    def get(self, request):        
        return Response({"login": "successful"})


class LogoutSuccess(APIView):

    def get(self, request):        
        return Response({"logout": "successful"})