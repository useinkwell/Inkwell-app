from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.Register.as_view(), name="register"),   

    path('posts/', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    
    path('membership/<int:pk>/', views.MembershipForUsername.as_view(), name='membership_username'),
    path('membership/', views.Membership.as_view(), name='membership'),

    path('<api_key>/account/<username>/', views.AccountInfoForUsername.as_view(), name='account_detail_username'),
    path('account/', views.AccountInfo.as_view(), name='account_detail'),
]
