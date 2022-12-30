from django.urls import path

from . import views

urlpatterns = [
    path('post/all/', views.PostList.as_view(), name='all_posts')
]
