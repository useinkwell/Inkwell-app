from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:user_name>/', consumers.ClientConsumer.as_asgi())
]