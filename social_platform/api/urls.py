from django.urls import path

from . import views


urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    
    path('membership/<int:pk>/', views.MembershipForUsername.as_view(), name='membership_username'),
    path('membership/', views.Membership.as_view(), name='membership'),

    path('account/<username>/', views.AccountInfoForUsername.as_view(), name='account_detail_username'),
    path('account/', views.AccountInfo.as_view(), name='account_detail'),
]
