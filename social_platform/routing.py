from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:user_name>/', consumers.UserConsumer.as_asgi())
]