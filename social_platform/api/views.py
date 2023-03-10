from django.shortcuts import render, redirect
import json
from django.conf import settings

# models
from social_platform.models import Post, Comment, Reaction, Following
from user.models import User
from django.contrib.contenttypes.models import ContentType

# serializers
from .serializers import PostSerializer, ReactionSerializer, CommentSerializer
from user.api.serializers import UserSerializer

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
from .permissions import (IsAdmin, IsAuthenticated, IsAdminElseReadOnly,
IsAuthenticatedElseReadOnly, IsPostAuthorElseReadOnly, IsReactorElseReadOnly,
IsCommentAuthorElseReadOnly)

# jwt authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.api.views import get_jwt_access_tokens_for_user

# Static/Media
from django.core.files.storage import FileSystemStorage

# pagination
from .pagination import PostPaginationConfig, CommentPaginationConfig

# signals
from social_platform.signals import new_following


class PostList(mixins.ListModelMixin, mixins.CreateModelMixin,
                                                generics.GenericAPIView):

    permission_classes = [IsAuthenticatedElseReadOnly]
    pagination_class = PostPaginationConfig
    ordering = '-id'

    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        # get dictionary equivalent of POST data and add additional data
        data = request.POST.dict()  # {'title': title, 'content': content,...}
        data['user'] = self.request.user

        print(f"ORDERED_DICT: {data}\n\n\n")

        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            # create a post instance using the POST data
            post = Post(**data)
            post.save()

            valid_data = serializer.data

            # image upload
            request_file_object = request.FILES['image']
            file_storage = FileSystemStorage()
            file_name = str(request_file_object).split('.')[0]
            stored_file = file_storage.save(file_name, request_file_object)
            file_url = file_storage.url(stored_file)
            valid_data["file"] = {"url": file_url}

            return Response(valid_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        # get the search term submitted with GET
        search_term = self.request.GET.get('search')
        filter = self.request.GET.get('filter')

        if search_term:
            # filter example format: <model field>__icontains=<search term>
            if filter == 'title':
                filtered_query = Post.objects.filter(
                                title__icontains=search_term).all()
            elif filter == 'category':
                filtered_query = Post.objects.filter(
                                category__icontains=search_term).all()
            elif filter == 'author':
                filtered_query = Post.objects.filter(
                        user__user_name__istartswith=search_term).all()
            elif filter == 'hashtag':
                filtered_query = Post.objects.filter(
                                hashtags__icontains=search_term).all()
            return filtered_query.order_by(PostList.ordering)
        else:
            # return this query if search field is empty (e.g on page load)
            return Post.objects.order_by(PostList.ordering).all()

     
class PostDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, generics.GenericAPIView):

    permission_classes = [IsPostAuthorElseReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    
class Membership(APIView):
    
    permission_classes = [IsAuthenticated]       

    def get(self, request):
    
        user = request.user
        if user.is_authenticated:
            serializer = UserSerializer(user)
            data = serializer.data
            
            response_data = {
                'membership': data['membership']
            }
            return Response(response_data)
        return Response({'error': 'no authentication'}, 
                                        status.HTTP_400_BAD_REQUEST)
 

class MembershipForUsername(APIView):

    permission_classes = [IsAdmin]          

    def get(self, request, pk):
        
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        data = serializer.data

        response_data = {
            'email': data['email'],
            'username': data['user_name'],            
            'membership': data['membership']
        }

        return Response(response_data)


class AccountInfo(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        serializer = UserSerializer(user)
        data = serializer.data
        response_data = {
            'id': data['id'],
            'username': data['user_name'],
            'email': data['email'],
            'membership': data['membership'],
            'image_file': data['image_file'],
            'access_tokens': get_jwt_access_tokens_for_user(user)
        }
        return Response(response_data)


class AccountInfoForUsername(APIView):

    permission_classes = [IsAdmin]

    def get(self, request, username):

        other_user = User.objects.get(user_name=username)

        if other_user and self.request.user.is_authenticated:
            serializer = UserSerializer(other_user)
            data = serializer.data
            response_data = {
                'id':data['id'],
                'username':data['user_name'],
                'email':data['email'],
                'membership':data['membership'],
                'image_file':data['image_file'],
                'access_tokens':'classified'
            }
        return Response(response_data)


class FollowUser(APIView):
    permission_classes = [IsAuthenticated]

    def send_follow_signal(self, instance, newly_created):
        new_following.send(
        sender=self.__class__,
        instance=instance,
        created=newly_created)

    def post(self, request, username):
        user_to_follow = User.objects.filter(user_name=username).first()
        if user_to_follow:
            if user_to_follow == self.request.user:
                return Response(
                    {"error": "can't follow self"}, 
                                status=status.HTTP_417_EXPECTATION_FAILED)

            following_instance, newly_created = Following.objects.get_or_create(
                follower=self.request.user,
                following=user_to_follow
            )

            # send signal to create follower activity
            if newly_created:
                FollowUser.send_follow_signal(
                    self, instance=following_instance, newly_created=True)

                return Response({'followed user': username}, 
                                    status=status.HTTP_200_OK)
            else:
                return Response({'user already follwed': username}, 
                                    status=status.HTTP_208_ALREADY_REPORTED)
        return Response({"error": "specified user doesn't exist"},
                                status=status.HTTP_417_EXPECTATION_FAILED)


class UnfollowUser(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user_to_unfollow = User.objects.filter(user_name=username).first()
        if user_to_unfollow:
            try:
                follow_relationship = Following.objects.filter(
                    follower=self.request.user,
                    following=user_to_unfollow).first()
                
                follow_relationship.delete()
            except AttributeError:
                return Response({"error": "currently not following user"},
                                status=status.HTTP_417_EXPECTATION_FAILED)
            return Response({'unfollowed user': username},
                                                status=status.HTTP_200_OK)
        return Response({"error": "user specified doesn't exist"},
                                status=status.HTTP_417_EXPECTATION_FAILED)


class ListFollowers(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        followers_object = self.request.user.followers.all()
        followers = map(lambda follower_instance: \
            follower_instance.follower.user_name, followers_object)
        data = {"followers": followers}
        return Response(data, status=status.HTTP_200_OK)


class ListFollowing(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_object = self.request.user.following.all()
        following = map(lambda following_instance: \
            following_instance.following.user_name, following_object)
        data = {"following": following}
        return Response(data, status=status.HTTP_200_OK)


class CheckFollowership(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        other_user = User.objects.filter(user_name=username).first()
        if other_user:
            current_user_follows_other = \
                            Following.objects.filter(
                                follower=self.request.user,
                                following=other_user).first()
            other_user_follows_current = \
                            Following.objects.filter(
                                follower=other_user,
                                following=self.request.user).first()

            followership = {
                'current_user_follows_other': bool(current_user_follows_other),
                'other_user_follows_current': bool(other_user_follows_current)
            }
            return Response(followership, status=status.HTTP_200_OK)
        return Response({"error": "couldn't fetch other user"},
                            status=status.HTTP_417_EXPECTATION_FAILED)


class React(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, model:str, instance_id:int, emoji:str):

        content_type = ContentType.objects.get(model=model.lower())
        object_reacted_on = content_type.get_object_for_this_type(id=instance_id)

        user = self.request.user
        is_duplicate_reaction = Reaction.objects.filter(user=user, emoji=emoji).first()
        if is_duplicate_reaction:
            return Response({emoji: f"already reacted by user on this {model}"},
                             status=status.HTTP_417_EXPECTATION_FAILED)

        # Create a new Reaction object for a specific Post/Comment object
        reaction = Reaction(
        content_type=content_type,
        object_id=object_reacted_on.id,
        content_object=object_reacted_on,
        user=user,
        emoji=emoji
        )
        reaction.save()

        response_data = {
            "reaction": emoji,
            "model": model,
            "instance_id": instance_id,
            "user": self.request.user.user_name
        }
        return Response(response_data, status=status.HTTP_200_OK)
        

class UnReact(APIView):

    # permission_classes: permission is tied to the logic for this view. Only 
    # user who reacted on an object can remove the reaction.

    def post(self, request, model:str, instance_id:int, emoji:str):

        content_type = ContentType.objects.get(model=model.lower())        
        object_reacted_on = content_type.get_object_for_this_type(id=instance_id)

        try:
            reaction = Reaction.objects.get(content_type=content_type,
                                            object_id=object_reacted_on.pk, 
                                            emoji=emoji, user=self.request.user)

        except Reaction.DoesNotExist:
            return Response(
                {"error": f"no '{emoji}' reaction from current user on this {model}"},
                                status=status.HTTP_404_NOT_FOUND)

        else:
            reaction.delete()        

        response_data = {
            "removed reaction": emoji
        }
        return Response(response_data, status=status.HTTP_200_OK)
        

class ReactList(APIView):

    # no permissions required for this view
    permission_classes = []

    def get(self, request, model:str, instance_id:int):

        content_type = ContentType.objects.get(model=model.lower())
        object_reacted_on = content_type.get_object_for_this_type(id=instance_id)

        reactions = Reaction.objects.filter(content_type=content_type, 
                        object_id=instance_id).all()

        serializer = ReactionSerializer(reactions, many=True)

        response_data = {
            "model": model,
            "instance_id": instance_id,
            "reactions": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class CommentList(mixins.ListModelMixin, mixins.CreateModelMixin,
                                                    generics.GenericAPIView):
    permission_classes = [IsAuthenticatedElseReadOnly]
    pagination_class = CommentPaginationConfig

    serializer_class = CommentSerializer
    ordering = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        class CommentNotForPost(Exception):
            pass

        try:
            post_id = self.kwargs['pk']
            post = Post.objects.get(pk=post_id)        
            parent_comment_id = self.request.GET.get('parent_comment')
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                if parent_comment.post.pk != post.pk:
                    raise CommentNotForPost
            else:
                parent_comment = None
            content = self.request.GET.get('content')
        except Comment.DoesNotExist:
            return Response({"error": "invalid parent_comment id"}, 
                                            status=status.HTTP_404_NOT_FOUND)
        except CommentNotForPost:
            return Response(
                {"error": f"post (id={post_id}) and parent_comment (post_id={parent_comment.post.pk}) do not match!"},
                                            status=status.HTTP_400_BAD_REQUEST)
        
        new_comment = Comment.objects.create(
            user=self.request.user,
            post=post,
            parent_comment=parent_comment,
            content=content
        )            

        serializer = CommentSerializer(new_comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        post_id = self.kwargs['pk']
        post = Post.objects.get(pk=post_id)
        comments = post.comments.order_by(CommentList.ordering).all()
        return comments
        

class CommentDetail(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
 mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    permission_classes = [IsCommentAuthorElseReadOnly]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        