from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    path('login-success/', views.LoginSuccess.as_view(), name="login-success"),
    path('logout-success/', views.LogoutSuccess.as_view(), name="logout-success"),

    path('post/<pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/all/', views.PostList.as_view(), name='all_posts'),
    path('membership/<pk>/', views.Membership.as_view(), name='membership'),
    path('membership/', views.Membership.as_view(), name='membership'),
    path('<api_key>/account/<username>/', views.AccountDetail.as_view(), name='account-detail'),
    path('post/new/<str:api_key>/', views.PostCreate.as_view(), name='post_create'),
]
