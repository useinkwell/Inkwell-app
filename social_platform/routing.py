from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:access_token>/', consumers.ClientConsumer.as_asgi())
]