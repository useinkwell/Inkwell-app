from django.urls import path

from . import views


urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),

    path('comments/post/<int:pk>/', views.CommentList.as_view(), name='comment_list'),
    path('comment/<int:pk>/', views.CommentDetail.as_view(), name='comment_detail'),

    path('react/add/<str:model>/<int:instance_id>/<str:emoji>/', views.React.as_view(), name='react'),
    path('react/remove/<str:model>/<int:instance_id>/<str:emoji>/', views.UnReact.as_view(), name='unreact'),
    path('react/list/<str:model>/<int:instance_id>/', views.ReactList.as_view(), name='react_list'),
    
    path('membership/<int:pk>/', views.MembershipForUsername.as_view(), name='membership_username'),
    path('membership/', views.Membership.as_view(), name='membership'),

    path('account/<username>/', views.AccountInfoForUsername.as_view(), name='account_detail_username'),
    path('account/', views.AccountInfo.as_view(), name='account_detail'),

    path('following/follow/<str:username>/', views.FollowUser.as_view(), name='follow'),
    path('following/unfollow/<str:username>/', views.UnfollowUser.as_view(), name='unfollow'),
    path('following/check/<str:username>/', views.CheckFollowership.as_view(), name='check_followership'),
    path('following/followers/', views.ListFollowers.as_view(), name='list_followers'),
    path('following/followed/', views.ListFollowing.as_view(), name='list_following'),
]
