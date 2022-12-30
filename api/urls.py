from django.urls import path

from . import views

urlpatterns = [
    path('post/<pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/all/', views.PostList.as_view(), name='all_posts'),
    path('membership/<pk>/', views.UserMembership.as_view(), name='membership'),
]
