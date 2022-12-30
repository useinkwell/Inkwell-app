from django.urls import path

from . import views

urlpatterns = [
    path('post/<pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/all/', views.PostList.as_view(), name='all_posts'),
    path('membership/<pk>/', views.UserMembership.as_view(), name='membership'),
    path('<api_key>/<username>/', views.AccountDetail.as_view(), name='account-detail'),
    path('post/new/<str:api_key>/', views.PostCreate.as_view(), name='post_create'),
]
