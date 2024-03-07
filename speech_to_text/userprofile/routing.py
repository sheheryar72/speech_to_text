# routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/speech-to-text/', consumers.SpeechToTextConsumer),
]
