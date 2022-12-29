from django.urls import path

from . import views

urlpatterns = [
    path('post/all/', views.posts_list, name='all_posts')
]
