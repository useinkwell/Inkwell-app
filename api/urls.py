from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('login/', views.LoginView.as_view(), name="login"),
    # path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    # path('login-success/', views.LoginSuccess.as_view(), name="login-success"),
    # path('logout-success/', views.LogoutSuccess.as_view(), name="logout-success"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', views.Register.as_view(), name="register"),   

    path('post/<pk>/', views.SpecificPost.as_view(), name='specific_post'),
    path('post/all/', views.PostList.as_view(), name='all_posts'),
    path('membership/<pk>/', views.MembershipForUsername.as_view(), name='membership_username'),
    path('membership/', views.Membership.as_view(), name='membership'),
    path('<api_key>/account/<username>/', views.AccountInfoForUsername.as_view(), name='account_detail_username'),
    path('account/', views.AccountInfo.as_view(), name='account_detail'),
    path('post/new/<str:api_key>/', views.PostCreate.as_view(), name='post_create'),
]
