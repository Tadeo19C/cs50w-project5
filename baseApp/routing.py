import os
from django.urls import re_path
from baseApp import consumers

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_name>\w+)/$', consumers.AudioConsumer.as_asgi()),
]